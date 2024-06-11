from Muice import Muice
import llm
import json,logging

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)  

logger = logging.getLogger(__name__)

logging.warning('由于协议库问题, 机器人登录可能失效。若您无法登录,请使用chatglm2-6b下的web_demo.sh运行本微调模型')

configs = json.load(open('configs.json','r',encoding='utf-8'))

if configs["model_loader"] == "api":
    model = llm.api(configs["model_name_or_path"])
elif configs["model_loader"] == "transformers":
    model = llm.transformers(configs["model_name_or_path"],configs["adapter_name_or_path")
elif configs["model_loader"] == "llmtuner":
    model = llm.llmtuner(configs["model_name_or_path"],configs["adapter_name_or_path")

muice_app = Muice(model, configs['read_memory_from_file'], configs['known_topic_probability'], configs['time_topic_probability'])
qqbot_app = QQBotFlaskApp(muice_app, configs)
qqbot_app.run(host = '127.0.0.1', port = configs['accept_post'])