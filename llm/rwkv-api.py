import requests as r
import json


class llm:
    """
    通过RWKV-RUNNER的api服务, 使用第三方RWKV模型
    """

    def __init__(self, url: str, *args, **kwargs):
        self.url = url + "/chat/completions"

    def ask(self, user_text: str, history: list, ):
        messages = []
        if history:
            for chat in history:
                messages.append({"role": "user", "content": chat[0], "raw": False})
                messages.append({"role": "assistant", "content": chat[1], "raw": False})

        messages.append({"role": "user", "content": user_text, "raw": False})
        response = r.post(self.url, json={
            "frequency_penalty": 1,
            "max_tokens": 1000,
            "messages": messages,
            "model": "Muice",
            "presence_penalty": 0,
            "presystem": True,
            "stream": False,
            "temperature": 1,
            "top_p": 0.3
        })

        response = json.loads(response.text)
        return response['choices'][0]["message"]["content"].lstrip()
