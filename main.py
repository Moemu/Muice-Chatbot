from Muice import Muice
from qqbot import qqbot
import json

#使用API模式调用模型
# from llm.api import Model
# model = Model('https://127.0.0.1:8000')
# 使用本地模式调用模型
from llm.chatglm2 import Model
model = Model('model/chatglm2-6b','model/Muice')

configs = json.load(open('configs.json','r',encoding='utf-8'))

muice = Muice(model, configs['read_memory_from_file'], configs['known_topic_probability'], configs['time_topic_probability'])

qqbot(muice, Trust_QQ_list=configs['Trust_QQ_list'], AutoCreateTopic=configs['AutoCreateTopic'])