from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys
from PIL import Image
import torch
import aiohttp
import logging
import asyncio
import io

class ImageCaptioningPipeline:
    _model = None

    @classmethod
    def load_model(cls, model_path):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logging.info("[ofa_image_process]: 加载模型中...")
        logging.info(f"[ofa_image_process]: 使用设备: {device}")
        cls._model = pipeline(Tasks.image_captioning, model=model_path)
        logging.info("[ofa_image_process]: 模型加载完成！")

    async def generate_caption(self, url):
        try:
            url = url.replace('&amp;', '&')
        except:
            pass
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                image_bytes = await response.read()
                image = Image.open(io.BytesIO(image_bytes))
        result = self._model(image)
        caption = result[OutputKeys.CAPTION][0]
        logging.info(f"[ofa_image_process]: 生成的图片描述: {caption}")
        caption = f"(收到图片描述：{caption})"
        return caption

