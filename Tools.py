import json
import re


class configs_tool:
    def __init__(self):
        self.configs = json.load(open('configs.json', 'r', encoding='utf-8'))

    def get(self, key):
        return self.configs.get(key)


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
