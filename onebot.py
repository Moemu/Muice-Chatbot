import logging
from flask import Flask, request, Response
import requests
import time
from command import Command
from apscheduler.schedulers.background import BackgroundScheduler  

class QQBotFlaskApp:
    def __init__(self, muice_app,configs):
        self.app = Flask(__name__)
        self.command = Command(muice_app) 

        self.command.load_default_command()
        

        self.muice_app = muice_app
        self.trust_qq_list = configs['Trust_QQ_list']
        self.auto_create_topic = configs['AutoCreateTopic']
        self.send_post = configs['send_post']
        self.time_dict = {qq_id: time.time() for qq_id in self.trust_qq_list}


        self.scheduler = BackgroundScheduler()  
        self.scheduler.add_job(self.timework, 'interval', minutes=1)  # 每分钟执行一次timework函数  
        self.scheduler.start()
        print(self.time_dict)
        

        @self.app.route('/', methods=['POST'])
        def qqbot():
            data = request.json
            sender_user_id = data.get('sender', {}).get('user_id')
            mess = ' '.join([item['data']['text'] for item in data['message'] if item['type'] == 'text'])
            logging.info(f'{sender_user_id} say: {mess}')
            if data.get('message_type') == "private" and sender_user_id and 'message' in data and sender_user_id in self.trust_qq_list: 
                self.reply_mess(mess, sender_user_id)
                return Response(status=200)
            return Response(status=404)


    def reply_mess(self, mess, sender_user_id):
        self.store_time(time.time(),sender_user_id)
        if not str(mess).strip():
                return None
        if str(mess).startswith('/'):
            reply = self.command.run(mess)
            self.prmess(prid=sender_user_id, messages=reply)
        else:
            reply = self.muice_app.ask(text=mess, user_qq=sender_user_id)
            for reply_item in reply:
                time.sleep(len(reply_item)*0.8)
                self.prmess(prid=sender_user_id, messages=reply_item)
                
            self.muice_app.finish_ask(str(reply))
        return None    

                
    def run(self, host='127.0.0.1', port=0000, debug=False):
        '''启动函数'''
        self.app.run(host=host, port=port, debug=debug)  


    def prmess( self,  prid , messages ):
        '''发送私聊消息'''
        url = "http://127.0.0.1:"+str(self.send_post)+"/send_private_msg"                      
        headers = {"content-type":"application/json",'Connection':'close'}
        mess = {"user_id":prid,"message":messages}
        res = requests.post(url, json = mess,headers=headers)
        return(res.text)
    
    def store_time(self, time, id):  
        """ 存储time_dict """  
        if id in self.time_dict:  
            # 如果id已存在，更新其time  
            if self.time_dict[id] < time:  # 假设time是可以比较大小的（如datetime对象）  
                self.time_dict[id] = time  
        else:  
            # 如果id不存在，添加新的键值对  
            self.time_dict[id] = time  
        return None 
    
    def timework(self):
        '''定时任务函数'''
        print(self.time_dict)
        for key,value in self.time_dict.items():  
            print(value)
            Topic = self.muice_app.CreateANewTopic(value)
            print(Topic)
            if Topic is None:
                return None
            else:
                mess = self.muice_app.ask(Topic, key)
                self.reply_mess(mess, key)
                return None



    def __del__(self):  
         if self.scheduler.running:  
            self.scheduler.shutdown()
      

  



    


  



