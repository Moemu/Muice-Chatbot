from llmtuner.chat import ChatModel


class llm:
    """
    使用LLaMA-Factory方案加载, 适合通过其他微调方案微调的模型加载
    """

    def __init__(self, model_name_or_path: str, adapter_name_or_path: str):
        self.model = ChatModel(dict(
            model_name_or_path=model_name_or_path,
            adapter_name_or_path=adapter_name_or_path,
            template="qwen"
        ))

    def ask(self, user_text: str, history: list, ):
        messages = []
        if history:
            for chat in history:
                messages.append({"role": "user", "content": chat[0]})
                messages.append({"role": "assistant", "content": chat[1]})
        messages.append({"role": "user", "content": user_text})
        response = self.model.chat(messages)
        return response[0].response_text
