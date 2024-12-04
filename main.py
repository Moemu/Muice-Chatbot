import importlib
import logging
import sys
import yaml

from Muice import Muice
from ws import QQBot

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


configs:dict = yaml.load(open('configs.yml', 'r', encoding='utf-8'),Loader=yaml.FullLoader)

# 模型配置
model_loader = configs['model']["loader"]
model_name_or_path = configs['model']["model_path"]
adapter_name_or_path = configs['model']["adapter_path"]

# 模型加载
model_adapter = importlib.import_module(f"llm.{model_loader}")
model = model_adapter.llm(model_name_or_path, adapter_name_or_path)

# Faiss配置
enable_faiss = configs['faiss']["enable"]
if enable_faiss:
    from llm.faiss_memory import FAISSMemory
    import signal
    memory = FAISSMemory(model_path=configs['faiss']["path"],db_path="./memory/faiss_index.faiss",top_k=2)
    def handle_interrupt(faiss_memory: FAISSMemory):
        """处理中断信号"""
        logging.info("接收到中断信号，正在保存数据...")
        faiss_memory.save_all_data()
        sys.exit(0)
    signal.signal(signal.SIGINT, lambda sig, frame: handle_interrupt(memory))
else:
    memory = None



# OFA图像模型
enable_ofa_image = configs["ofa_image"]['enable']
if enable_ofa_image:
    from utils.ofa_image_process import ImageCaptioningPipeline
    ofa_image_model_name_or_path = configs["ofa_image"]['path']
    ImageCaptioningPipeline.load_model(ofa_image_model_name_or_path)

# QQBot
muice_app = Muice(model, memory, configs)
qqbot_app = QQBot(muice_app)
qqbot_app.run()
