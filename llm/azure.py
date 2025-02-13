import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from llm.utils.auto_system_prompt import auto_system_prompt

class llm:
    def __init__(self, model_config: dict):
        self.model_name = model_config.get("model_name", "DeepSeek-R1")
        self.system_prompt = model_config.get("system_prompt", None)
        self.auto_system_prompt = model_config.get("auto_system_prompt", False)
        self.user_instructions = model_config.get("user_instructions", None)
        self.max_tokens = model_config.get("max_tokens", 1024)
        self.temperature = model_config.get("temperature", None)
        self.top_p = model_config.get("top_p", None)
        self.frequency_penalty = model_config.get("frequency_penalty", None)
        self.presence_penalty = model_config.get("presence_penalty", None)
        self.think = model_config.get("think", 0)
        try:
            self.token = os.environ["GITHUB_TOKEN"]
        except KeyError:
            self.token = model_config.get("token", None)
        self.endpoint = "https://models.inference.ai.azure.com"
        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.token),
        )

    def ask(self, user_text: str, history: list):
        if self.auto_system_prompt:
            self.system_prompt = auto_system_prompt(user_text)
        if self.system_prompt:
            messages = [SystemMessage(self.system_prompt)]
        else:
            messages = []
        for h in history:
            messages.append(UserMessage(h[0]))
            messages.append(AssistantMessage(h[1]))
        if self.user_instructions and len(history) == 0:
            messages.append(UserMessage(self.user_instructions + '\n' + user_text))
        else:
            messages.append(UserMessage(user_text))
        response = self.client.complete(messages=messages, model=self.model_name,
                                        max_tokens=self.max_tokens,
                                        temperature=self.temperature,
                                        top_p=self.top_p, 
                                        frequency_penalty=self.frequency_penalty, 
                                        presence_penalty=self.presence_penalty)
        response_content = response.choices[0].message.content
        return response_content