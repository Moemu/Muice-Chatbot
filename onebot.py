import logging
from flask import Flask, request, Response
import requests

from command import Command

class QQBotFlaskApp:
    def __init__(self, muice_app, trust_qq_list, auto_create_topic, send_post):
        self.app = Flask(__name__)
        self.command = Command(muice_app) 
        self.command.load_default_command()

        self.muice_app = muice_app
        self.trust_qq_list = trust_qq_list
        self.auto_create_topic = auto_create_topic
        self.send_post = send_post

        @self.app.route('/', methods=['POST'])
        def qqbot():
            data = request.json
            sender_user_id = data.get('sender', {}).get('user_id')
            mess = ' '.join([item['data']['text'] for item in data['message'] if item['type'] == 'text'])
            if data.get('message_type') == "private":  # 移除不必要的默认值
                
                if sender_user_id and 'message' in data:
                    logging.info(f"{sender_user_id}: {mess}")

                    if sender_user_id in trust_qq_list:
                        self.reply_mess(mess, sender_user_id)
                return Response(status=200)


    def reply_mess(self, mess, sender_user_id):
        if not mess.strip():
            return
        if mess.startswith('/'):
            reply = self.command.run(mess)
            self.prmess(prid=sender_user_id, messages=reply)
        else:
            reply = self.muice_app.ask(text=mess, user_qq=sender_user_id)
            for reply_item in reply:
                self.prmess(prid=sender_user_id, messages=reply_item)

            try:
                self.muice_app.finish_ask(str(reply))
            except Exception as e:
                logging.error(f"finish_ask_error: {e}") 
                #这玩意,,留个报错吧,反正也没啥用(
                

    def run(self, host='0.0.0.0', port=8080, debug=False):
        '''启动函数'''
        self.app.run(host=host, port=port, debug=debug)  

    def prmess( self,  prid , messages ):
        '''发送私聊消息'''
        url = "http://127.0.0.1:"+str(self.send_post)+"/send_private_msg"                      
        headers = {"content-type":"application/json",'Connection':'close'}
        mess = {"user_id":prid,"message":messages}
        res = requests.post(url, json = mess,headers=headers)
        return(res.text)              


    


  



