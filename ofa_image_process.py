from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys
from PIL import Image
import torch
import aiohttp
import logging
import asyncio
import io
import ssl

class ImageCaptioningPipeline:
    _model = None

    @classmethod
    def load_model(cls, model_path):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logging.info("[ofa_image_process]: 加载模型中...")
        logging.info(f"[ofa_image_process]: 使用设备: {device}")
        cls._model = pipeline(Tasks.image_captioning, model=model_path)
        logging.info("[ofa_image_process]: 模型加载完成！")

    @classmethod
    def unload_model(cls):
        if cls._model is not None:
            del cls._model
            cls._model = None
            torch.cuda.empty_cache()  # 释放显存
            logging.info("[ofa_image_process]: 模型已卸载，显存已释放！")
        else:
            logging.info("[ofa_image_process]: 没有模型需要卸载。")

    async def generate_caption(self, url):
        try:
            url = url.replace('&amp;', '&')
        except:
            pass
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers('DEFAULT@SECLEVEL=1')
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=ssl_context) as response:
                image_bytes = await response.read()
                image = Image.open(io.BytesIO(image_bytes))
        result = self._model(image)
        caption = result[OutputKeys.CAPTION][0]
        logging.info(f"[ofa_image_process]: 生成的图片描述: {caption}")
        caption = f"(收到图片描述：{caption})"
        return caption

