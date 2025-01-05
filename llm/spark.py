import websocket
import json
import logging
from llm.utils.auto_system_prompt import auto_system_prompt

logger = logging.getLogger('Muice')

class llm:
    """
    星火大模型
    """

    def __init__(self, model_path:str, adapter_path:str, system_prompt:str, auto_system_prompt:bool, *args, **kwargs):
        self.app_id =  args[0]['app_id']
        self.service_id = args[0]['service_id']
        self.resource_id = args[0]['resource_id']
        self.url = "wss://maas-api.cn-huabei-1.xf-yun.com/v1.1/chat"
        self.system_prompt = system_prompt
        self.auto_system_prompt = auto_system_prompt
        self.response = ''
        self.is_history = False

    def __on_message(self, ws, message):
        response = json.loads(message)
        logger.debug(f"Spark返回数据: {response}")
        if response['header']['status'] in [0, 2] and response['payload']['choices']['text'][0]['content'] != ' ':
            self.response += response['payload']['choices']['text'][0]['content']
        if response['header']['status'] == 2:
            ws.close()
        if response['header']['status'] == 1:
            logger.error(f"调用Spark在线模型时发生错误: {response}")
            ws.close()

    def __on_error(self, ws, error):
        logger.error(f"调用Spark在线模型时发生错误: {error}")

    def __on_close(self, ws, close_status_code, close_msg):
        pass

    def __on_open(self, ws):
        request_data = {
            "header": {
                "app_id": self.app_id,
                "patch_id": [self.resource_id]
            },
            "parameter": {
                "chat": {
                    "domain": self.service_id,
                    "temperature": 0.85
                }
            },
            "payload": {
                "message": {
                    "text": self.history
                }
            }
        }
        ws.send(json.dumps(request_data))

    def generate_system_prompt(self, user_text: str) -> str:
        if self.auto_system_prompt:
            return 'system\n\n' + auto_system_prompt(user_text) + 'user\n\n'
        return 'system\n\n' + self.system_prompt + 'user\n\n'
    
    def generate_history(self, history: list):
        self.history = []
        for item in history:
            self.history.append({"role": 'user', "content": self.generate_system_prompt(item[0]) + item[0]})
            self.history.append({"role": 'assistant', "content": item[1]})
            self.is_history = True

    def ask(self, user_text: str, history: list):
        self.generate_history(history)
        if not self.is_history:
            self.history.append({"role": 'user', "content": self.generate_system_prompt(user_text) + user_text})
        else:
            self.history.append({"role": 'user', "content": user_text})
        self.response = ''

        ws = websocket.WebSocketApp(self.url,
                                    on_message=self.__on_message,
                                    on_error=self.__on_error,
                                    on_close=self.__on_close)
        ws.on_open = self.__on_open
        ws.run_forever(ping_timeout=10)

        return self.response