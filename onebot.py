import logging
from flask import Flask, request, Response
import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler  

from command import Command
import onebot_def 


class QQBotFlaskApp:
    def __init__(self, muice_app,configs):
        self.app = Flask(__name__)
        self.command = Command(muice_app) 
        


        self.commands = []
        self.commands_function = []
        self.Muice = muice_app
        

        self.muice_app = muice_app
        self.trust_qq_list = configs['Trust_QQ_list']
        self.auto_create_topic = configs['AutoCreateTopic']
        self.send_post = configs['send_post']
        self.time_dict = {qq_id: time.time() for qq_id in self.trust_qq_list}
        self.mess = ""
        self.sender_id = ""


        self.scheduler = BackgroundScheduler()  
        self.scheduler.add_job(self.timework, 'interval', minutes=23)  # 每23分钟执行一次timework函数  
        self.scheduler.start()
        self.load_default_command()
        

        @self.app.route('/', methods=['POST'])
        def qqbot():
            data = request.json
            self.sender_id = data.get('sender', {}).get('user_id')
            self.mess = ' '.join([item['data']['text'] for item in data['message'] if item['type'] == 'text'])
            logging.info(f'{self.sender_id} say: {self.mess}')
            if data.get('message_type') == "private" and self.sender_id and 'message' in data and self.sender_id in self.trust_qq_list: 
                self.reply_mess()
                return Response(status=200)
            return Response(status=404)

    def run(self, host='127.0.0.1', port=0000, debug=False):
        '''启动函数'''
        self.app.run(host=host, port=port, debug=debug)  



    def resister_command(self,command:str,command_function):
        '''
        注册命令
        Args:
            command: 命令字符串
            command_function: 所执行的函数
        '''
        self.commands.append(command)
        self.commands_function.append(command_function)


    def load_default_command(self):
        '''
        加载默认命令
        '''
        self.resister_command('/help',self.command.default_help)
        self.resister_command('/refresh',self.command.refresh)
        self.resister_command('/clean',self.command.clean)
        self.resister_command('/reset',self.command.reset)
        self.resister_command('/undo',self.command.undo)
        self.resister_command('/restart',self.command.restart)
        self.resister_command('/echo',self.command.echo)  
        self.resister_command('/Audio',self.Audio)  

    def command_run(self,mess_self) -> str:
        '''
        执行命令，返回命令命令执行结果或命令不存在的提示
        '''
        parts = mess_self.mess.split(' ')
    # 如果分割后有多于一个的部分，则返回第一个部分，否则返回原字符串
        mess = parts[0] if len(parts) > 1 else mess_self.mess
        for i in range(len(self.commands)):
            if self.commands[i] == mess:
                return self.commands_function[i](mess_self)
        return self.command.no_command()





    def reply_mess(self):
        print(self.send_post)
        if not str(self.mess).strip():
                return None
        if str(self.mess).startswith('/'):
            reply = self.command_run(mess_self = self)
            onebot_def.prmess(prid=self.sender_id, messages=reply, send_post=self.send_post)
        else:
            reply = self.muice_app.ask(text=self.mess, user_qq=self.sender_id)
            for reply_item in reply:
                time.sleep(len(reply_item)*0.8)
                onebot_def.prmess(prid=self.sender_id, messages=reply_item, send_post=self.send_post)  
                self.store_time()    
            self.muice_app.finish_ask(str(reply))
        return None    

    def store_time(self):  
        """ 存储time_dict """  
        id = self.sender_id  
        if id in self.time_dict:  
            # 如果id已存在，更新其time  
            if self.time_dict[id] < time.time():
                self.time_dict[id] = time.time()  
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


    def Audio(self,mess_self):   
             
      

  



    


  



