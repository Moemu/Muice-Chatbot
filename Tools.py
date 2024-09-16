import json
import logging
import re


class configs_tool:
    def __init__(self, level=3):
        self.configs = json.load(open('configs.json', 'r', encoding='utf-8'))
        self.default_configs = json.load(open('./advanced_tool/default_configs.json', 'r', encoding='utf-8'))
        self.check_configs = json.load(open('./advanced_tool/check_configs.json', 'r', encoding='utf-8'))
        self.level = level

    def get(self, key):
        if self.level == 1:
            logging.debug(f"获取键：{key},值为：{self.configs.get(key)}")

        if key in self.configs:
            value = self.configs.get(key)
            if self.level <= 4:
                if self.check_key(key, value):
                    return value
                return None
            return value
        elif key in self.default_configs:
            logging.debug(f"获取默认参数：{key},值为：{self.default_configs.get(key)}")
            return self.default_configs.get(key)
        else:
            logging.error(f"请求了错误的键：{key},请确认您的配置文件是否正确")
            return None

    def check_key(self, key, value):
        if key not in self.check_configs:
            logging.error(f"无法检查{key}类型，请检查您的配置文件是否正确")
            return True
        value_type = self.check_configs.get(key)
        actual_type = type(value).__name__
        # logging.debug(f"检查{key}类型，期望类型为{value_type},实际类型为{actual_type}")
        if value_type == actual_type:
            return True
        else:
            logging.error(f"配置文件参数{key}的值类型为{actual_type},但期望类型为{value_type}")
            return False


async def build_msg_reply_json(reply_message, user_id, action):
    """构建回复的消息的json"""
    if reply_message is None:
        return None
    if action == 'send_private_msg':
        send_id = "user_id"
    else:
        send_id = "group_id"

    data = {
        "action": action,
        "params": {
            send_id: user_id,
            "message": reply_message
        }
    }
    return json.dumps(data, ensure_ascii=False)


async def process_data(data):
    return


def divide_sentences(text: str) -> list:
    """
    切分一段句子
    """
    sentences = re.findall(r'.*?[~。！？…]+', text)
    if len(sentences) == 0:
        return [text]
    return sentences



