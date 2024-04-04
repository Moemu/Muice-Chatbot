import time
from flask import Flask, request ,Response   
from command import Command  
from apscheduler.schedulers.background import BackgroundScheduler  
from apscheduler.triggers.interval import IntervalTrigger
import defqq 
from Muice import Muice  

# Flask配置
class flask():
    def __init__(self, Muice: Muice, Trust_QQ_list: list, AutoCreateTopic: False):
        self.Muice = Muice
        self.Trust_QQ_list = Trust_QQ_list
        self.AutoCreateTopic = AutoCreateTopic
        self.port = 8010     #onebot-http监听端口
        self.app = Flask(__name__)
        if self.AutoCreateTopic:
            self.automess = Flask(__name__)
            # 定时任务调度器 
            scheduler = BackgroundScheduler()  
            scheduler.start()
            scheduler.add_job(self.CreateANewChat, IntervalTrigger(seconds=120))
            self.automess.run(debug=True)

    def CreateANewChat(self):  
        '''  
        主动发起对话  
        '''  
        topic = Muice.CreateANewTopic()  
        reply = Muice.ask(topic, self.Trust_QQ_list[0])  
        if reply != '':
            for st in reply:  
                time.sleep(3)  
                if st == '' or st == ' ':  
                    continue  
                defqq.prmess(prid=self.Trust_QQ_list[0], messages=st, port=self.port)        
                print(f'主动发送消息{self.Trust_QQ_list[0]}: {st}') 

    def load_app(self):
        @self.app.route('/', methods=['POST'])
        def post():  
            data = request.json
            if not data.get('message_type', {}) == "private":
                return Response(status=404)
            command = Command(Muice)
            command.load_default_command()    
            mess = ' '.join([item['data']['text'] for item in data['message'] if item['type'] == 'text'])  
            sender_user_id = data.get('sender', {}).get('user_id')
            if not sender_user_id in self.Trust_QQ_list:
                return
            print(str(sender_user_id) + ": " + mess)
            is_command, result = command.run(mess)
            #print(str(is_command)+"*****"+str(result))  
            if is_command and result:  
                reply = result  
            elif is_command:  
                reply = "操作已完成"  
            else:  
                reply = self.Muice.ask(text=mess, user_qq=sender_user_id)  
            try:
                if not type(reply) == list:
                    print(f'不支持的回复类型: {reply}')
                    return
                for st in reply:
                    if st == '' or st == ' ':
                        continue
                    if not is_command:
                        time.sleep(len(st)*0.8)
                        defqq.prmess(prid=sender_user_id, messages=st, port=self.port)        
                        print(f'发送消息{sender_user_id}: {st}')
                        time.sleep(3)
                    elif type(reply) == str and not reply in ['',' ']:
                        if not is_command:
                            time.sleep(len(st)*0.8)
                            defqq.prmess(prid=sender_user_id, messages=reply, port=self.port)    
                            print(f'回复{sender_user_id}: {reply}')                       
                Muice.finish_ask(reply,is_command)
            except Exception as e:
                print(e)
        return self.app