import importlib
import json
import logging

from Muice import Muice
from ws2 import BotWebSocket

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)

configs = json.load(open('configs.json', 'r', encoding='utf-8'))

# 模型配置
model_loader = configs["model_loader"]
model_name_or_path = configs["model_name_or_path"]
adapter_name_or_path = configs["adapter_name_or_path"]

# 模型加载
model = importlib.import_module(f"llm.{model_loader}")
model = model.llm(model_name_or_path, adapter_name_or_path)

# QQBot
muice_app = Muice(model, configs['read_memory_from_file'], configs['known_topic_probability'],
                  configs['time_topic_probability'])
ws = BotWebSocket(muice_app)
ws.run()
