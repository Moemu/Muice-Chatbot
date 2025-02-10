import requests as r
import json


class llm:
    """
    通过RWKV-RUNNER的api服务, 使用第三方RWKV模型
    """
    def __init__(self, model_config: dict):
        self.host = model_config.get("host", "http://localhost:5000")
        self.model = model_config.get("model", "Muice")
        self.temperature = model_config.get("temperature", 1)
        self.top_p = model_config.get("top_p", 0.3)
        self.max_tokens = model_config.get("max_tokens", 1000)
        self.presence_penalty = model_config.get("presence_penalty", 0)


    def ask(self, user_text: str, history: list, ):
        messages = []
        if history:
            for chat in history:
                messages.append({"role": "user", "content": chat[0], "raw": False})
                messages.append({"role": "assistant", "content": chat[1], "raw": False})

        messages.append({"role": "user", "content": user_text, "raw": False})
        response = r.post(self.host, json={
            "frequency_penalty": self.presence_penalty,
            "max_tokens": self.max_tokens,
            "messages": messages,
            "model": self.model,
            "presence_penalty": self.presence_penalty,
            "presystem": True,
            "stream": False,
            "temperature": self.temperature,
            "top_p": self.top_p
        })

        response = json.loads(response.text)
        return response['choices'][0]["message"]["content"].lstrip()
