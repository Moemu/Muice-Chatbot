import logging
import os
import torch

from transformers import AutoTokenizer, AutoModel, AutoConfig


class llm:
    """
    使用transformers方案加载, 适合通过P-tuning V2方式微调的模型加载
    """

    def __init__(self, chatglm_model_path: str, pt_model_path: str):
        model_path = chatglm_model_path
        config = AutoConfig.from_pretrained(model_path, trust_remote_code=True, pre_seq_len=128)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        if torch.cuda.is_available():
            model = AutoModel.from_pretrained(model_path, config=config, trust_remote_code=True).cuda()
        else:
            logging.info("未检测到GPU,将使用CPU进行推理")
            model = AutoModel.from_pretrained(model_path, config=config, trust_remote_code=True).float()
        prefix_state_dict = torch.load(os.path.join(pt_model_path, "pytorch_model.bin"), map_location='cpu')
        new_prefix_state_dict = {}
        for k, v in prefix_state_dict.items():
            if k.startswith("transformer.prefix_encoder."):
                new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
        model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)
        model.transformer.prefix_encoder.float()
        self.model = model.eval()

    def ask(self, user_text: str, history: list, ) -> str:
        response, _ = self.model.chat(self.tokenizer, user_text, history=history)
        return response

    def doc(self):
        return {"is_Agent":False,"doc":"使用transformers方案加载, 适合通过P-tuning V2方式微调的模型加载"}