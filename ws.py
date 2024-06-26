from fastapi import FastAPI, WebSocket  
from starlette.websockets import WebSocketDisconnect 
import json,time  
from command import Command
from Tools import divide_sentences
from apscheduler.schedulers.background import BackgroundScheduler  
import asyncio
import uvicorn 
import logging

  


class QQBot:  
    def __init__(self,muice_app):  
        self.app = FastAPI()  
        self.muice_app = muice_app
        
        self.command = Command(muice_app)
        self.command.load_default_command()
        
        
        self.configs = json.load(open('configs.json','r',encoding='utf-8'))
        self.trust_qq_list = self.configs['Trust_QQ_list']
        self.websocket_port = self.configs['port']
        self.auto_create_topic = self.configs['AutoCreateTopic']
        if self.auto_create_topic:
            self.time_dict = {qq_id: time.time() for qq_id in self.trust_qq_list}
            self.scheduler = BackgroundScheduler()  
            self.scheduler.add_job(self.timework, 'interval', minutes=1)  
            self.scheduler.start()
            self.websocket = None
  
        

        @self.app.websocket("/ws/api")  
        async def websocket_endpoint(websocket: WebSocket):  
            await websocket.accept() 
            if self.auto_create_topic:
                self.websocket = websocket
            try: 
                #链接请求 
                while True:  
                    data = await websocket.receive_text()   
                    reply = await self.processing_json(data) 
                    if reply is None:
                        continue 
                    logging.info(f"回复{reply}")
                    await websocket.send_text(reply) 
            except WebSocketDisconnect:  
                logging.info("WebSocket disconnected")   
        
    async def processing_json(self,data):  
        '''解析json并返回需发送的消息'''
        data = json.loads(data) 
        logging.debug(f"收到{data}") 
  
        if 'post_type' in data and data['post_type'] == 'meta_event':  
            if data['meta_event_type'] == 'lifecycle':  
                if data['sub_type'] == 'connect':  
                    logging.info(f"已链接")
                    return None 
            elif data['meta_event_type'] == 'heartbeat':  
                    return None  
            
        elif 'post_type' in data and data['post_type'] == 'message':  
            '''消息处理'''
            sender_user_id = data.get('sender', {}).get('user_id')
            message = ' '.join([item['data']['text'] for item in data['message'] if item['type'] == 'text'])
            logging.info(f"收到{sender_user_id}的消息：{message}")
            reply_message = await self.produce_reply(message, sender_user_id)
            reply = await self.build_reply_json(reply_message,sender_user_id) 
            return reply 
        else: 
            return None
    
    
    
    async def build_reply_json(self, reply_message, sender_user_id):
        if reply_message is None:
                return None
        data = {
                "action": "send_private_msg",
                "params": {
                    "user_id": sender_user_id,
                    "message": reply_message
                    }
                }
        return json.dumps(data, ensure_ascii=False)           
  
  
    async def produce_reply(self, mess, sender_user_id):
        if self.auto_create_topic:
            await self.store_time(sender_user_id)
        if not str(mess).strip():
                return None
        if str(mess).startswith('/'):
            reply = self.command.run(mess)
            return reply
        else:
            reply = self.muice_app.ask(text=mess, user_qq=sender_user_id)
            reply_list = divide_sentences(reply)
            self.muice_app.finish_ask(reply_list)
            for reply_item in reply_list:
                await asyncio.sleep(len(reply_item)*0.8)
                return reply_item
        return None    
    
    async def store_time(self, id):  
        """ 存储time_dict """  
        if id in self.time_dict:   
            if self.time_dict[id] < time.time():  
                self.time_dict[id] = time.time()  
        else:   
            self.time_dict[id] = time.time()  
        return None   
    def run(self): 
        uvicorn.run(self.app, host="127.0.0.1", port=self.websocket_port)
    def timework(self):
        '''定时任务函数'''
        print(self.time_dict)
        for key,value in self.time_dict.items():  
            Topic = self.muice_app.CreateANewTopic(value)
            if Topic is None:
                continue 
            else:
                mess = self.muice_app.ask(Topic, key)
                reply = self.produce_reply(mess, key)
                self.websocket.send_text(reply)  
                return None
            
     

  
  
if __name__ == '__main__':
    Muice_app = None
    ws = QQBot(Muice_app)
    ws.run()