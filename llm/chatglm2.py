from transformers import AutoTokenizer, AutoModel, AutoConfig
import torch,os


class Model():
    '''
    使用p-tuningV2微调的chatglm2-6b模型
    '''
    def __init__(self,chatglm_model_path:str, pt_model_path:str):
        device = torch.device(0)
        model_path = chatglm_model_path
        config = AutoConfig.from_pretrained(model_path, trust_remote_code=True, pre_seq_len=128)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        model = AutoModel.from_pretrained(model_path, config=config, trust_remote_code=True).half().to(device)
        prefix_state_dict = torch.load(os.path.join(pt_model_path, "pytorch_model.bin"))
        new_prefix_state_dict = {}
        for k, v in prefix_state_dict.items():
            if k.startswith("transformer.prefix_encoder."):
                new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
        model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)
        model = model.half().cuda()
        model.transformer.prefix_encoder.float()
        self.model = model.eval()

    def ask(self,user_text:str, history:list,):
        response, _ = self.model.chat(self.tokenizer, user_text, history=history)
        return response