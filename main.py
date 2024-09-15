import importlib
import json
import logging
from Tools import configs_tool

from Muice import Muice
from ws import BotWebSocket

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)


configs_tool = configs_tool(logger.level)

configs = json.load(open('configs.json', 'r', encoding='utf-8'))

# 模型配置
model_loader = configs["model_loader"]
model_name_or_path = configs["model_name_or_path"]
adapter_name_or_path = configs["adapter_name_or_path"]

# 模型加载
chat_model = importlib.import_module(f"llm.{model_loader}")
chat_model = chat_model.llm(model_name_or_path, adapter_name_or_path)
muice_app = Muice(chat_model, configs['read_memory_from_file'], configs['known_topic_probability'],
                  configs['time_topic_probability'])

other_model = None

ws = BotWebSocket(configs_tool)
ws.initialize_model(chat_model, other_model)
ws.run()
