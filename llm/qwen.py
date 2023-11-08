from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer

class Model():
    '''
    使用Qlora微调的qwen-7B微调模型
    '''
    def __init__(self, qwen_qlora_model:str):
        self.tokenizer = AutoTokenizer.from_pretrained(qwen_qlora_model,device_map="auto",trust_remote_code=True)
        model = AutoPeftModelForCausalLM.from_pretrained(qwen_qlora_model,device_map="auto",trust_remote_code=True).eval()
        self.model = model.eval()

    def ask(self,user_text:str, history:list,):
        response, _ = self.model.chat(self.tokenizer, user_text, history=history)
        return response