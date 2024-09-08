import asyncio
import json
import logging
import time
import uvicorn

from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from fish_speech_api import fish_speech_api
from Tools import divide_sentences
from Tools import process_at_message
from Tools import is_reply_message
from Tools import is_image_message
from Tools import voice_message_reply
from command import Command


async def build_reply_json(reply_message, sender_user_id):
    """构建回复的消息的json"""
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


async def build_group_reply_json(reply_message, group_id):
    """构建回复的消息的json"""
    if reply_message is None:
        return None
    data = {
        "action": "send_group_msg",
        "params": {
            "group_id": group_id,
            "message": reply_message
        }
    }
    return json.dumps(data, ensure_ascii=False)


class QQBot:
    def __init__(self, muice_app):
        self.app = FastAPI()
        self.muice_app = muice_app

        self.command = Command(muice_app)
        self.command.load_default_command()

        # 配置获取
        self.configs = json.load(open('configs.json', 'r', encoding='utf-8'))
        self.trust_qq_list = self.configs.get('Trust_QQ_list', [])
        self.websocket_port = self.configs.get('port')
        self.is_cq_code = self.configs.get('Is_CQ_Code', False)
        self.bot_qq_id = self.configs.get('bot_qq_id')
        self.reply_rate = self.configs.get('Reply_Rate', 100)
        self.at_reply = self.configs.get('At_Reply', False)
        self.nonreply_prefix = self.configs.get('NonReply_Prefix', [])
        self.enable_ofa_image = self.configs.get('enable_ofa_image', False)
        self.voice_reply_rate = self.configs.get('Voice_Reply_Rate', 0)
        self.reply_wait = self.configs.get('Reply_Wait', True)
        # 主动对话
        self.auto_create_topic = self.configs.get('AutoCreateTopic', False)
        if self.auto_create_topic:
            from apscheduler.schedulers.asyncio import AsyncIOScheduler
            self.time_dict = {qq_id: time.time() for qq_id in self.trust_qq_list}
            self.scheduler = AsyncIOScheduler()
            self.scheduler.add_job(self.time_work, 'interval', minutes=1)
            self.websocket = None
        # 群聊消息
        self.group_message_reply = self.configs.get('Group_Message_Reply', False)
        if self.group_message_reply:
            self.group_message_reply_list = self.configs.get('Trust_QQ_Group_list', [])
            self.group_reply_only_to_trusted = self.configs.get('Group_Message_Reply_Only_To_Trusted', True)
            self.TEST_New_Group_Memory = self.configs.get('TEST_New_Group_Memory', False)
            logging.debug(f"group_message_reply_list = {self.group_message_reply_list}"
                          f"group_reply_only_to_trusted = {self.group_reply_only_to_trusted}"
                          f"TEST_New_Group_Memory = {self.TEST_New_Group_Memory}")

        # 定义公共变量
        self.is_at_message = False
        if self.enable_ofa_image:
            from ofa_image_process import ImageCaptioningPipeline
            self.image_captioning_pipeline = ImageCaptioningPipeline()

        @self.app.websocket("/ws/api")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            if self.auto_create_topic:
                self.websocket = websocket
                self.scheduler.start()
            try:
                # 链接请求
                while True:
                    data = await websocket.receive_text()
                    result = await self.processing_reply(data)
                    if result is not None:
                        reply_list, sender_user_id, group_id = result

                        if group_id == -1:
                            for reply_item in reply_list:
                                if self.reply_wait:
                                    await asyncio.sleep(len(reply_item) * 0.6)
                                if reply_item is None:
                                    continue
                                logging.debug(f"回复{reply_item}")
                                reply_json = await build_reply_json(reply_item, sender_user_id)
                                await websocket.send_text(reply_json)
                        elif group_id is not None:
                            for reply_item in reply_list:
                                # await asyncio.sleep(len(reply_item) * 0.8)  #在群聊环境中不使用等等
                                if reply_item is None:
                                    continue
                                logging.debug(f"回复{reply_item}")
                                reply_json = await build_group_reply_json(reply_item, group_id)
                                await websocket.send_text(reply_json)

            except WebSocketDisconnect:
                logging.info("WebSocket disconnected")

        @self.app.on_event("shutdown")
        async def shutdown():
            if self.scheduler is not None and self.scheduler.running:
                self.scheduler.shutdown()

    async def processing_reply(self, data):
        """解析消息json并返回需发送的消息"""
        try:
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

                if self.is_cq_code:
                    '''对于某些基于 OneBot 协议的插件输出的消息为字符串的情况'''
                    message = data['message']

                    '''检查是否为图片消息并输出URL'''
                    if self.enable_ofa_image:
                        is_image,image_url = is_image_message(message)
                    else:
                        is_image = False

                else:
                    ''' 检查 data['message'] 是否为列表'''
                    if not isinstance(data['message'], list):
                        logging.error("消息格式错误: data['message'] 不是列表")
                        return None
                    
                    ''' 处理图片消息 '''
                    image_url = None
                    is_image = False
                    for msg in data.get('message', []):
                        if msg.get('type') == 'image':
                            image_url = msg['data'].get('url')
                            is_image = True
                            message = data['raw_message']
                            break
                    
                    if not is_image:
                        message = ' '.join([item['data']['text'] for item in data['message'] if item['type'] == 'text'])
                    else:
                        if not self.enable_ofa_image:
                            logging.info("收到图片消息，但未开启图片回复功能")
                            return None

                if data['message_type'] == 'private':
                    logging.info(f"收到QQ{sender_user_id}的消息：{message}")
                    if sender_user_id in self.trust_qq_list:
                        if is_image: message = await self.image_captioning_pipeline.generate_caption(image_url)
                        reply_message_list = await self.produce_reply(message, sender_user_id)
                        if reply_message_list:
                            logging.debug(f"回复list{reply_message_list}")
                            if reply_message_list is None:
                                return None
                            return reply_message_list, sender_user_id, -1
                        else:
                            return None

                elif data['message_type'] == 'group' and self.group_message_reply:
                    group_id = data.get('group_id')
                    logging.info(f"收到群{group_id}QQ{sender_user_id}的消息：{message}")

                    if self.is_cq_code:
                        ''' 对消息中的 at 信息进行处理过滤 '''
                        self.is_at_message,at_matches,message = process_at_message(message)
                        if at_matches:
                            if str(self.bot_qq_id) not in at_matches:
                                logging.info(f"消息中@不是机器人，已过滤")
                                return None
                        else:
                            if self.at_reply:
                                logging.info(f"消息中未@机器人，已过滤")
                                return None
                    else:
                        at_qq_list = []
                        for msg in data.get('message', []):
                            if msg.get('type') == 'at':
                                at_qq_list.append(msg['data']['qq'])
                                if msg['data']['qq'] == str(self.bot_qq_id):
                                    self.is_at_message = True
                                    break
                        if at_qq_list and str(self.bot_qq_id) not in at_qq_list:
                            logging.info(f"消息中@不是机器人，已过滤")
                            return None
                        if not self.is_at_message:
                            if self.at_reply:
                                logging.info(f"消息中未@机器人，已过滤")
                                return None
                            
                    if group_id in self.group_message_reply_list:
                        if self.group_reply_only_to_trusted:
                            if sender_user_id in self.trust_qq_list:
                                if not is_reply_message(self.at_reply,self.reply_rate,self.is_at_message): logging.info(f"未达到消息回复率{self.reply_rate}%，不回复") ; return None
                                if is_image: message = await self.image_captioning_pipeline.generate_caption(image_url)
                                reply_message_list = await self.produce_group_reply(message, sender_user_id, group_id)
                                logging.debug(f"回复list{reply_message_list}")
                                if reply_message_list is None:
                                    return None
                                return reply_message_list, sender_user_id, group_id
                            else:
                                return None
                        else:
                            if not is_reply_message(self.at_reply,self.reply_rate,self.is_at_message): logging.info(f"未达到消息回复率{self.reply_rate}%，不回复") ; return None
                            if is_image: message = await self.image_captioning_pipeline.generate_caption(image_url)
                            reply_message_list = await self.produce_group_reply(message, sender_user_id, group_id)
                            logging.debug(f"回复list{reply_message_list}")
                            if reply_message_list is None:
                                return None
                            return reply_message_list, sender_user_id, group_id
                    else:
                        return None
                else:
                    return None
            else:
                return None
        except json.JSONDecodeError:
            logging.error("JSON解析错误")
            return None
        except Exception as e:
            logging.error(f"处理消息时发生错误: {e}")
            logging.error(f"接收到的数据: {json.dumps(data, ensure_ascii=False, indent=4)}")
            return None

    async def produce_reply(self, mess, sender_user_id) -> list | None:
        """ 回复消息 """
        if self.auto_create_topic:
            await self.store_time(sender_user_id)
        if not str(mess).strip():
            return [] #None会导致reply_list为空，导致TypeError: 'NoneType' object is not iterable
        '''检测是否匹配前缀'''
        for prefix in self.nonreply_prefix:
            if str(mess).startswith(prefix):
                return []
        if str(mess).startswith('/'):
            reply = self.command.run(mess)
            reply_list = divide_sentences(reply)
            return reply_list
        else:
            reply = self.muice_app.ask(text=mess, user_qq=sender_user_id, group_id=-1)
            logging.info(f"回复消息：{reply}")
            reply_list = divide_sentences(reply)
            self.muice_app.finish_ask(reply_list)
            if voice_message_reply(self.voice_reply_rate):
                logging.info(f"尝试回复语音消息")
                try:
                    voice_file = await fish_speech_api(reply)
                    reply_list = [f'[CQ:record,file=file:///{voice_file}]']
                except Exception as e:
                    logging.error(f"回复语音消息失败: {e}")
            return reply_list

    async def produce_group_reply(self, mess, sender_user_id, group_id) -> list | None:
        """ 回复消息群聊 """
        if not str(mess).strip():
            if self.is_at_message:
                mess="在吗"#待定，中文语境中单at含义与在吗相似
            else:
                return []
        '''检测是否匹配前缀'''
        for prefix in self.nonreply_prefix:
            if str(mess).startswith(prefix):
                return []
        if str(mess).startswith('/'):
            reply = self.command.run(mess)
            reply_list = divide_sentences(reply)
            return reply_list
        else:
            reply = self.muice_app.ask(text=mess, user_qq=sender_user_id, group_id=group_id)
            logging.info(f"回复消息：{reply}")
            reply_list = divide_sentences(reply)
            self.muice_app.finish_ask(reply_list)
            if voice_message_reply(self.voice_reply_rate):
                logging.info(f"尝试回复语音消息")
                try:
                    voice_file = await fish_speech_api(reply)
                    reply_list = [f'[CQ:record,file=file:///{voice_file}]']
                except Exception as e:
                    logging.error(f"回复语音消息失败: {e}")
            return reply_list

    async def store_time(self, user_id):
        """ 存储time_dict """
        if user_id in self.time_dict:
            if self.time_dict[user_id] < time.time():
                self.time_dict[user_id] = time.time()
        else:
            self.time_dict[user_id] = time.time()
        return None

    async def time_work(self):
        """定时任务函数"""
        for key, value in self.time_dict.items():
            topic = self.muice_app.create_a_new_topic(value)
            if topic is None:
                continue
            else:
                mess = self.muice_app.ask(topic, key)
                reply = await build_reply_json(mess, key)
                await self.websocket.send_text(reply)

    def run(self):
        uvicorn.run(self.app, host="127.0.0.1", port=self.websocket_port)


if __name__ == '__main__':
    logging.warning("用户请勿直接运行此文件，请使用main.py运行")
    Muice_app = None
    ws = QQBot(Muice_app)
    ws.run()