from transformers import AutoTokenizer, AutoModel, AutoConfig
from llmtuner.chat import ChatModel
import requests as r
import torch,os,logging
import json

class api():
    '''
    使用已经存在的API, 这个API应该接受prompt和history两个参数, 返回response
    '''
    def __init__(self,url:str):
        self.url = url

    def ask(self,user_text:str, history:list,):
        response = r.post(self.url,json={"prompt": user_text, "history": history})
        response = json.loads(response.text)
        return response['response']
    

class llmtuner():
    '''
    使用LLaMA-Factory方案加载, 适合通过其他微调方案微调的模型加载
    '''
    def __init__(self, model_name_or_path:str, adapter_name_or_path:str):
        self.model = ChatModel(dict(
        model_name_or_path = model_name_or_path,
        adapter_name_or_path = adapter_name_or_path,
        template="qwen"
        ))
        
    def ask(self,user_text:str, history:list,):
        messages = []
        if history != []:
            for chat in history:
                messages.append({"role": "user", "content":chat[0]})
                messages.append({"role": "assistant", "content":chat[1]})
        messages.append({"role": "user", "content": user_text})
        response = self.model.chat(messages)
        return response[0].response_text


class transformers():
    '''
    使用transformers方案加载, 适合通过P-tuning V2方式微调的模型加载
    '''
    def __init__(self,chatglm_model_path:str, pt_model_path:str):
        model_path = chatglm_model_path
        if 'checkpoint-3000' in os.listdir(pt_model_path):
            pt_model_path = os.path.join(pt_model_path, 'checkpoint-3000')
        config = AutoConfig.from_pretrained(model_path, trust_remote_code=True, pre_seq_len=128)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        if torch.cuda.is_available():
            model = AutoModel.from_pretrained(model_path, config=config, trust_remote_code=True).cuda()
        else:
            logging.warning("未检测到GPU,将使用CPU进行推理")
            model = AutoModel.from_pretrained(model_path, config=config, trust_remote_code=True).float()
        prefix_state_dict = torch.load(os.path.join(pt_model_path, "pytorch_model.bin"),map_location='cpu')
        new_prefix_state_dict = {}
        for k, v in prefix_state_dict.items():
            if k.startswith("transformer.prefix_encoder."):
                new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
        model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)
        model.transformer.prefix_encoder.float()
        self.model = model.eval()

    def ask(self,user_text:str, history:list,):
        response, _ = self.model.chat(self.tokenizer, user_text, history=history)
        return response
