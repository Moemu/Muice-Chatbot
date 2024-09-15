import requests as r
import json
import logging


class llm:
    """
    使用已经存在的API, 这个API应该接受prompt和history两个参数, 返回response
    """

    def __init__(self, url: str, *args, **kwargs):
        self.url = url

    def ask(self, user_text: str, history: list, ):
        response = r.post(self.url, json={"prompt": user_text, "history": history})
        response = json.loads(response.text)
        return response['response']

    def doc(self):
        logging.warning("当前为api加载,请确定使用当前方法")
        return {"is_Agent":False,"doc":"api加载"}