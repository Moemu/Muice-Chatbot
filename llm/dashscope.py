import dashscope
import logging
from llm.utils.auto_system_prompt import auto_system_prompt

logger = logging.getLogger('Muice')

class llm:
    def __init__(self, config: dict):
        self.api_key = config.get("api_key")
        self.model = config.get("model_name", "qwen-plus")
        self.max_tokens = config.get("max_tokens", 1024)
        self.temperature = config.get("temperature", 0.7)
        self.top_p = config.get("top_p", None)
        self.repetition_penalty = config.get("repetition_penalty", None)
        self.system_prompt = config.get("system_prompt", None)
        self.auto_system_prompt = config.get("auto_system_prompt", False)

    def ask(self, prompt, history=None) -> str:
        messages = []

        if self.auto_system_prompt:
            self.system_prompt = auto_system_prompt(prompt)
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        if history:
            for h in history:
                messages.append({"role": "user", "content": h[0]})
                messages.append({"role": "assistant", "content": h[1]})
        messages.append({"role": "user", "content": prompt})

        response = dashscope.Generation.call(
            api_key=self.api_key,
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            repetition_penalty=self.repetition_penalty
        )

        return response.output.text