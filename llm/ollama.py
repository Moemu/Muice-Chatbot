import ollama

class llm:
    """
    使用 Ollama 模型服务调用模型
    """

    # def __init__(self, model, host='http://localhost:11434'):
    def __init__(self, model_config: dict):
        self.model = model_config.get("model_path", "")
        host = model_config.get("host", 'http://localhost:11434')
        self.client = ollama.Client(host=host)

    def ask(self, user_text: str, history: list):
        messages = []
        if history:
            for chat in history:
                messages.append({"role": "user", "content": chat[0]})
                messages.append({"role": "assistant", "content": chat[1]})
        messages.append({"role": "user", "content": user_text})
        print(self.client)
        response = self.client.chat(self.model, messages)
        print(response)
        return response.message.content