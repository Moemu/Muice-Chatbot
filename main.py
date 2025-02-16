import importlib
import logging
import sys

from Muice import Muice
from ws import QQBot
from utils.logging import init_logger
import utils.configs as config


logger = init_logger(logging.INFO)

logger.warning("2025.02.10更新：由于配置文件格式变更，如果先前你拉取过本 Repo 并在 02.10 后执行过fetch操作，请您重新设置模型配置，由此带来的不便我们深表歉意")
logger.info("启动Muice-Chatbot中🚀...")

# 加载配置文件
logger.info("加载配置文件...")
configs = config.get()

# 模型配置
model_config = configs['model']

# 模型加载
logger.info(f"加载模型：{model_config.get('loader')}")
model_adapter = importlib.import_module(f"llm.{model_config.get('loader')}")
model = model_adapter.llm(model_config)

# Faiss配置
enable_faiss = configs['faiss']["enable"]
if enable_faiss:
    logger.info(f"加载Faiss记忆组件...")
    from llm.utils.faiss_memory import FAISSMemory
    import signal
    memory = FAISSMemory(model_path=configs['faiss']["path"], db_path="./memory/faiss_index.faiss", top_k=2)
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
    logger.info(f"加载OFA图像模型...")
    from utils.ofa_image_process import ImageCaptioningPipeline
    ofa_image_model_name_or_path = configs["ofa_image"]['path']
    ImageCaptioningPipeline.load_model(ofa_image_model_name_or_path)

# ws服务
logger.info("初始化Bot服务...")
muice_app = Muice(model, memory, configs)
ws_app = QQBot(muice_app, configs)
ws_app.run()
