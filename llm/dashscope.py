import dashscope
import logging
import pathlib
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
        self.user_instructions = config.get("user_instructions", None)
        self.auto_user_instructions = config.get("auto_user_instructions", False)

    def ask(self, prompt, history=None) -> str:
        messages = []

        if self.auto_system_prompt:
            self.system_prompt = auto_system_prompt(prompt)
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        if self.auto_user_instructions:
            self.user_instructions = auto_system_prompt(prompt)

        for index,value in enumerate(history):
            if index == 0 and self.user_instructions:
                messages.append({"role": "user", "content": self.user_instructions + '\n' + value[0]})
            else:
                messages.append({"role": "user", "content": value[0]})
            messages.append({"role": "assistant", "content": value[1]})
        
        if self.user_instructions and not history:
            messages.append({"role": "user", "content": self.user_instructions + '\n' + prompt})
        else:
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

        if self.model in ['deepseek-r1']:
            return '<think>' + response.output.choices[0].message.reasoning_content + '</think>' + response.output.choices[0].message.content

        return response.output.text
    
    def query_image(self, image_path: str) -> str:
        if not (image_path.startswith("http") or image_path.startswith("file")):
            abs_path = pathlib.Path(image_path).resolve()
            image_path = abs_path.as_uri()
            image_path = image_path.replace("file:///", "file://")
        message = [{"role": "user", "content": [{'image': image_path}, {'text': '描述图片'}]}]
        response = dashscope.MultiModalConversation.call(
            api_key=self.api_key,
            model=self.model,
            messages=message
        )
        return response["output"]["choices"][0]["message"].content[0]["text"]