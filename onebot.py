import json,logging,os,traceback,time
from flask import Flask, request ,Response  
from llm.chatglm2 import Model   
from command import Command  
from apscheduler.schedulers.background import BackgroundScheduler  
from apscheduler.triggers.interval import IntervalTrigger


import defqq 
from Muice import Muice  


#修改自main.py~

# 初始化相关对象和加载命令  
try:
    #使用API模式调用模型
    # from llm.api import Model
    # model = Model('https://127.0.0.1:8000')
    # 使用本地模式调用模型
    # 加载Qlora微调的qwen-7B模型
    # from llm.qwen import Model
    # model = Model('./model/Muice')
    from llm.chatglm2 import Model
    if os.path.exists('model/chatglm2-6b'):
        model = Model('model/chatglm2-6b','model/Muice')
    else:
        model = Model('model/chatglm2-6b-int4','model/Muice')
except OSError:
    logging.error('模型加载失败, 请检查是否在model目录下放置了初始模型与微调模型')
    traceback.print_exc()
    exit()
except:
    logging.error('模型加载失败！相关报错信息如下:')
    traceback.print_exc()
    exit()

configs = json.load(open('configs.json','r',encoding='utf-8'))

muice = Muice(model, configs['read_memory_from_file'], configs['known_topic_probability'], configs['time_topic_probability'])

Trust_QQ_list=configs['Trust_QQ_list']
AutoCreateTopic=configs['AutoCreateTopic']

#刚刚学py,如有错误请见谅

port = 8010     #onebot-http监听端口

app = Flask(__name__)  
  
 
def qqbot(Muice: Muice, Trust_QQ_list: list, AutoCreateTopic: False):  
    command = Command(Muice)
    command.load_default_command()             
    @app.route('/', methods=['POST'])  
    
    def add_post():  
        data = request.json  
        
 
  
        if data.get('message_type', {}) == "private":  
            mess = ' '.join([item['data']['text'] for item in data['message'] if item['type'] == 'text'])  
            sender_user_id = data.get('sender', {}).get('user_id')
            if sender_user_id in Trust_QQ_list:                 
                 print(str(sender_user_id) + ": " + mess)
                 is_command, result = command.run(mess)
                 #print(str(is_command)+"*****"+str(result))  
                 if is_command and result:  
                     reply = result  
                 elif is_command:  
                     reply = "操作已完成"  
                 else:  
                     reply = muice.ask(text=mess, user_qq=sender_user_id)  

                 try:
                    if type(reply) == list:           
                       for st in reply:
                            if st == '' or st == ' ':
                             continue
                            if not is_command:
                               time.sleep(len(st)*0.8)
                            defqq.prmess(prid=sender_user_id, messages=st, port=port)        
                            print(f'发送消息{sender_user_id}: {st}')
                            time.sleep(3)

                    elif type(reply) == str and not reply in ['',' ']:
                        if not is_command:
                           time.sleep(len(st)*0.8)

                        defqq.prmess(prid=sender_user_id, messages=reply, port=port)    
                        print(f'回复{sender_user_id}: {reply}')
                    else:
                           print(f'不支持的回复类型: {reply}')

                    Muice.finish_ask(reply,is_command)

                 except Exception as e:
                    print(e)
            # else :    
                 #print("非信任用户")
  
       
  
        return Response(status=404)
    
 
    

  
    # 返回 Flask 应用，以便在外部调用 run  
    return app  





automess = Flask(__name__)  
  
# 定时任务调度器  
scheduler = BackgroundScheduler()  
scheduler.start()  
  
def CreateANewChat():  
    '''  
    主动发起对话  
    '''  
    topic = Muice.CreateANewTopic()  
    reply = Muice.ask(topic, Trust_QQ_list[0])  
    if reply != '':  
        for st in reply:  
            time.sleep(3)  
            if st == '' or st == ' ':  
                continue  
            defqq.prmess(prid=Trust_QQ_list[0], messages=st, port=port)        
            print(f'主动发送消息{Trust_QQ_list[0]}: {st}') 
  
scheduler.add_job(CreateANewChat, IntervalTrigger(seconds=120))
#这里代码不太会,且不会测试,但愿能正常运行qwq




  
# 如果当前脚本是直接运行的，而不是被导入的，则创建并运行 Flask 
if __name__ == '__main__':  
    qqbot_app = qqbot(muice, Trust_QQ_list=configs['Trust_QQ_list'], AutoCreateTopic=configs['AutoCreateTopic']) 
    qqbot_app.run(host='127.0.0.1', port=8020)  # 运行 Flask #http事件上报端口应为http://127.0.0.1:8020
    automess.run(debug=True)
    
    
