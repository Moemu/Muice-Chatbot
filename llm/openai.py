import openai
import requests
from utils.logging import init_logger

logger = init_logger('Muice.LLM.OpenAI')

class llm:
    # def __init__(self, api_key, api_base=None, model="text-davinci-003", max_tokens=1024, temperature=0.7):
    def __init__(self, config: dict):

        self.api_key = config.get("api_key")
        self.api_base = config.get("api_base", "https://api.openai.com/v1")  # 默认的 OpenAI API 基地址
        self.model = config.get("model", "text-davinci-003")
        self.max_tokens = config.get("max_tokens", 1024)
        self.temperature = config.get("temperature", 0.7)

        # 配置 OpenAI API 密钥和基础 URL
        openai.api_key = self.api_key
        openai.api_base = self.api_base

    def ask(self, prompt, history=None):
        """
        向 OpenAI 模型发送请求，并获取模型的推理结果

        :param prompt: 输入给模型的文本
        :param history: 之前的对话历史（可选）
        :return: 模型生成的文本
        """
        try:
            full_prompt = "\n".join(history + [prompt]) if history else prompt
            response = openai.Completion.create(
                model=self.model,
                prompt=full_prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            # 获取并返回模型生成的文本
            return response.choices[0].text.strip()
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API 错误: {e}", exc_info=True)
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {e}", exc_info=True)
        return None