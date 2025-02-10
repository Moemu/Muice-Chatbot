from llmtuner.chat import ChatModel
from llm.utils.auto_system_prompt import auto_system_prompt

class llm:
    """
    使用LLaMA-Factory方案加载, 适合通过其他微调方案微调的模型加载
    """
    def __init__(self, model_config:dict):
        model_name_or_path = model_config.get("model_path", None)
        adapter_name_or_path = model_config.get("adapter_path", None)
        template = model_config.get("template", "qwen")
        self.system_prompt = model_config.get("system_prompt", None)
        self.auto_system_prompt = model_config.get("auto_system_prompt", False)
        self.max_tokens = model_config.get("max_tokens", 1024)
        self.temperature = model_config.get("temperature", 0.7)
        self.top_p = model_config.get("top_p", 0.9)
        self.model = ChatModel(dict(
            model_name_or_path=model_name_or_path,
            adapter_name_or_path=adapter_name_or_path,
            template=template,
        ))

    def ask(self, user_text: str, history: list):
        messages = []
        if self.auto_system_prompt:
            self.system_prompt = auto_system_prompt(user_text)
        if history:
            for chat in history:
                messages.append({"role": "user", "content": chat[0]})
                messages.append({"role": "assistant", "content": chat[1]})
        messages.append({"role": "user", "content": user_text})
        response = self.model.chat(messages, system = self.system_prompt, max_tokens = self.max_tokens, temperature = self.temperature, top_p = self.top_p)
        return response[0].response_text
