import requests as r
import json

class Model():
    '''
    使用已经存在的API, 这个API应该接受prompt和history两个参数, 返回response
    '''
    def __init__(self,url:str):
        self.url = url

    def ask(self,user_text:str, history:list,):
        response = r.post(self.url,json={"prompt": user_text, "history": history})
        response = json.loads(response.text)
        return response['response']