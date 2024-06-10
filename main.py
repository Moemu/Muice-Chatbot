from Muice import Muice
from qqbot import qqbot
import llm
import json,logging

logging.warning('10.14更新：由于协议库问题, 机器人登录可能失效。若您无法登录,请使用chatglm2-6b下的web_demo.sh运行本微调模型')

configs = json.load(open('configs.json','r',encoding='utf-8'))
model_loader = configs["model_loader"]
model_name_or_path = configs["model_name_or_path"]
adapter_name_or_path = configs["adapter_name_or_path"]

if model_loader == "api":
    model = llm.api(model_name_or_path)
elif model_loader == "transformers":
    model = llm.transformers(model_name_or_path,adapter_name_or_path)
elif model_loader == "llmtuner":
    model = llm.llmtuner(model_name_or_path,adapter_name_or_path)

muice = Muice(model, configs['read_memory_from_file'], configs['known_topic_probability'], configs['time_topic_probability'])

qqbot(muice, Trust_QQ_list=configs['Trust_QQ_list'], AutoCreateTopic=configs['AutoCreateTopic'])