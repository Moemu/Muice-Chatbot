import logging

import uvicorn
from fastapi import FastAPI, WebSocket
import asyncio


from process_message import process_message
from Tools import build_msg_reply_json


class BotWebSocket:
    def __init__(self, configs_tool, chat_model, other):
        """获取配置"""
        self.ws = None
        self.configs_tool = configs_tool
        self.ws_host = self.configs_tool.get('Ws_Host')
        self.ws_port = self.configs_tool.get('Ws_Port')
        self.wait_time = self.configs_tool.get('reply_wait_time')

        self.auto_create_topic = self.configs_tool.get('AutoCreateTopic')

        self.process_message_func = process_message(chat_model, self.configs_tool)
        self.app = FastAPI()
        self.received_messages_queue = asyncio.Queue()
        self.messages_to_send_queue = asyncio.Queue()

        @self.app.websocket("/ws/api")
        async def websocket_endpoint(websocket: WebSocket):

            await websocket.accept()
            self.ws = websocket
            asyncio.create_task(self.reply_messages())
            asyncio.create_task(self.create_messages())
            asyncio.create_task(self.active_message())
            # 这里 不要 await!!
            # 啊 pyc的警告请忽略

            try:
                async for message in websocket.iter_text():
                    await self.received_messages_queue.put(message)
                    print(f"Received: {message}")
            except Exception as e:
                print(f"WebSocket disconnected: {e}")

    async def reply_messages(self):
        """从消息队列取出消息传入处理,处理后加入发送队列"""
        while True:
            try:
                print("reply_messages")
                data = await self.received_messages_queue.get()
                # data格式如下:{"group_id": -1, "message_list": ["1", "2"], "sender_user_id": 114514}
                processed_message = await self.process_message_func.reply_message(data)
                if processed_message is not None:
                    await self.messages_to_send_queue.put(processed_message)

                self.received_messages_queue.task_done()
            except:
                continue

    async def create_messages(self):
        """从发送队列取出消息发送"""
        while True:
            try:
                print("send_messages")
                data = await self.messages_to_send_queue.get()
                logging.debug(f'data:{data}')

                await self.send_message(data)  # 分类发送消息
                self.messages_to_send_queue.task_done()
            except:
                continue

    async def send_message(self, data):
        if data is None:
            return None
        group_id = data.get('group_id', -1)
        reply_list = data.get('message_list', [])
        if not reply_list:
            return None
        reply_type = data.get('type', 'msg')
        logging.debug(f'发送列表:{reply_list}')
        if reply_list is None:
            return None
        if reply_type == 'msg':
            if group_id == -1:
                qq_id = data['sender_user_id']
                is_group_or_private = "send_private_msg"
            else:
                qq_id = data['group_id']
                is_group_or_private = "send_group_msg"
            for msg in reply_list:
                await asyncio.sleep(len(msg) * self.wait_time)
                message_json = await build_msg_reply_json(msg, qq_id, is_group_or_private)
                logging.info(f'发送消息{msg}')
                await self.ws.send_text(message_json)
        # 在此拓展type类型发送
        return None

    async def active_message(self):
        while self.auto_create_topic:
            auto_create_topic_result = self.process_message_func.auto_create_topic()
            for qq_id, msg in auto_create_topic_result:
                message_json = await build_msg_reply_json(msg, qq_id, "send_private_msg")
                logging.info(f'主动发送消息{msg}')
                await self.ws.send_text(message_json)
            await asyncio.sleep(60)

    def run(self):
        uvicorn.run(self.app, host=self.ws_host, port=self.ws_port)


if __name__ == '__main__':
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)
    logging.warning("用户请勿直接运行此文件，请使用main.py运行")
    logging.warning("用户请勿直接运行此文件，请使用main.py运行")
    logging.warning("用户请勿直接运行此文件，请使用main.py运行")
    from Tools import configs_tool
    configs = configs_tool(5)
    ws = BotWebSocket(configs,None,None)
    ws.run()
