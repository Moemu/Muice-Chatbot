import importlib
import logging
import sys
import yaml

from Muice import Muice
from ws import QQBot
from utils.logging import init_logger


logger = init_logger(logging.INFO)

logger.warning("2024.12.04更新：由于配置文件格式变更，如果先前你拉取过本Repo并在12.04后执行过fetch操作，请您重新设置配置文件，由此带来的不便我们深表歉意")

configs:dict = yaml.load(open('configs.yml', 'r', encoding='utf-8'),Loader=yaml.FullLoader)

# 模型配置
model_loader = configs['model']["loader"]
model_name_or_path = configs['model']["model_path"]
adapter_name_or_path = configs['model']["adapter_path"]
system_prompt = configs['model']["system_prompt"]
auto_system_prompt = configs['model']["auto_system_prompt"]

# 模型加载
logger.info(f"正在加载模型：{model_loader}: {model_name_or_path}")
model_adapter = importlib.import_module(f"llm.{model_loader}")
model = model_adapter.llm(model_name_or_path, adapter_name_or_path, system_prompt, auto_system_prompt)

# Faiss配置
enable_faiss = configs['faiss']["enable"]
if enable_faiss:
    from llm.faiss_memory import FAISSMemory
    import signal
    memory = FAISSMemory(model_path=configs['faiss']["path"],db_path="./memory/faiss_index.faiss",top_k=2)
    def handle_interrupt(faiss_memory: FAISSMemory):
        """处理中断信号"""
        logger.info("接收到中断信号，正在保存数据...")
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
