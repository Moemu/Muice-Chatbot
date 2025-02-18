import asyncio
import yaml
import logging
import time
import uvicorn
import json

from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from utils.fish_speech_api import fish_speech_api
from utils.Tools import is_command
from utils.Tools import divide_sentences
from utils.Tools import process_at_message
from utils.Tools import is_reply_message
from utils.Tools import is_image_message
from utils.Tools import voice_message_reply
from utils.Tools import get_nickname
from utils.command import Command
from llm.utils.thought import process_thoughts

logger = logging.getLogger('Muice')

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
    def __init__(self, muice_app, configs:dict):
        self.app = FastAPI()
        self.muice_app = muice_app

        self.command = Command(muice_app)
        self.command.load_default_command()

        # 配置获取
        self.configs = configs
        self.websocket_port = self.configs.get('bot', {}).get('port', 21050)
        self.is_cq_code = self.configs.get('bot', {}).get('cq_code', False)
        self.bot_qq_id = self.configs.get('bot', {}).get('id', "")
        self.reply_rate = self.configs.get('bot', {}).get('group', {}).get('rate', 0.5)
        self.at_reply = self.configs.get('bot', {}).get('group', {}).get('only_at', True)
        self.nonreply_prefix = self.configs.get('bot', {}).get('nonreply_prefix', [])
        self.enable_ofa_image = self.configs.get('ofa_image', {}).get('enable', False)
        self.enable_multi_modal = self.configs.get('multimodal', {}).get('enable', False)
        self.voice_reply_rate = self.configs.get('voice_reply', {}).get('rate', 0.75)
        self.reply_wait = self.configs.get('bot', {}).get('wait_reply', True)
        self.auto_create_topic = self.configs.get('active', {}).get('enable', False)
        self.targets = self.configs.get('active', {}).get('targets', [])
        self.nickname = self.configs.get('bot', {}).get('nickname', '观众大大')

        if self.auto_create_topic:
            from apscheduler.schedulers.asyncio import AsyncIOScheduler
            self.time_dict = {qq_id: time.time() for qq_id in self.targets}
            self.scheduler = AsyncIOScheduler()
            self.scheduler.add_job(self.time_work, 'interval', minutes=1)
            self.websocket = None

        if self.configs.get('bot', {}).get('anyone', False):
            self.trust_qq_list = []
        else:
            self.trust_qq_list = self.configs.get('bot', {}).get('trusted', [])

        # 群聊消息
        self.group_message_reply = self.configs.get('bot', {}).get('group', {}).get('enable', False)
        if self.group_message_reply:
            self.group_anyone = self.configs.get('bot', {}).get('group', {}).get('anyone', False)
            self.group_message_reply_list = self.configs.get('bot', {}).get('group', {}).get('trusted', [])
            self.group_reply_only_to_trusted = self.configs.get('bot', {}).get('group', {}).get('only_trusted', False)
            self.group_cmd_for_trusted_users_only = self.configs.get('bot', {}).get('group', {}).get('cmd_only_trusted', False)

        # 定义公共变量
        self.is_at_message = False
        if self.enable_ofa_image:
            from utils.ofa_image_process import ImageCaptioningPipeline
            self.image_captioning_pipeline = ImageCaptioningPipeline()
            from utils.image_database import ImageDatabase
            self.image_db = ImageDatabase()

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
                    logger.debug(f"收到数据：{data}")
                    result = await self.processing_reply(data)
                    if result is not None:
                        reply_list, sender_user_id, group_id = result

                        if group_id == -1:
                            for reply_item in reply_list:
                                if self.reply_wait:
                                    if not is_image_message(True,reply_item)[0]:
                                        await asyncio.sleep(len(reply_item) * 0.6)
                                if reply_item is None:
                                    continue
                                logger.debug(f"发送：{reply_item}")
                                reply_json = await build_reply_json(reply_item, sender_user_id)
                                await websocket.send_text(reply_json)
                        elif group_id is not None:
                            for reply_item in reply_list:
                                # await asyncio.sleep(len(reply_item) * 0.8)  #在群聊环境中不使用等等
                                if reply_item is None:
                                    continue
                                logger.debug(f"发送：{reply_item}")
                                reply_json = await build_group_reply_json(reply_item, group_id)
                                await websocket.send_text(reply_json)
                                await asyncio.sleep(0.5) # 避免消息过快导致发送顺序错乱

            except WebSocketDisconnect:
                logger.warning("失去与QQ的WebSocket连接")

        @self.app.on_event("shutdown")
        async def shutdown():
            if self.scheduler is not None and self.scheduler.running:
                self.scheduler.shutdown()

    async def processing_reply(self, data):
        """解析消息json并返回需发送的消息"""
        try:
            data = json.loads(data)

            if 'post_type' in data and data['post_type'] == 'meta_event':
                if data['meta_event_type'] == 'lifecycle':
                    if data['sub_type'] == 'connect':
                        logger.info(f"沐雪Chatbot已在运行中✨")
                        return None
                elif data['meta_event_type'] == 'heartbeat':
                    return None

            elif 'post_type' in data and data['post_type'] == 'message':
                '''消息处理'''
                sender_user_id = data.get('sender', {}).get('user_id')
                qq_nickname = data.get('sender', {}).get('nickname')
                self.nickname = get_nickname(self.nickname, qq_nickname, data['message_type'] == 'group')

                is_image, image_url = is_image_message(self.is_cq_code, data)
                if is_image and not (self.enable_ofa_image or self.enable_multi_modal):
                    logger.info("捕获到图片消息，但未开启图片回复功能，已跳过")
                    return None
                if self.is_cq_code:
                    '''对于CQ码消息处理'''
                    message = data['message']
                else:
                    ''' 检查 data['message'] 是否为列表'''
                    if not isinstance(data['message'], list):
                        logger.error("消息格式错误: data['message'] 不是列表，疑似CQ码消息")
                        return None
                    message = ' '.join([item['data']['text'] for item in data['message'] if item['type'] == 'text'])


                if data['message_type'] == 'private':
                    if not is_image:
                        logger.info(f"收到来自QQ{sender_user_id}的消息：{message}")
                    else:
                        logger.info(f"收到来自QQ{sender_user_id}的图片消息")

                    if (sender_user_id not in self.trust_qq_list) and (self.trust_qq_list != []):
                        return None
                    
                    if is_image:
                        if self.enable_multi_modal:
                            message = self.muice_app.image_query(image_url)
                            logger.info(f"图片描述：{message}")
                            message = f"<收到图片描述：{message}>"

                        elif self.enable_ofa_image:
                            message = await self.image_captioning_pipeline.generate_caption(image_url)
                            await self.image_db.insert_data(message, image_url)
                            logger.info(f"图片描述：{message}")
                            message = f"<收到图片描述：{message}>"
                    
                    reply_message_list = await self.produce_reply(message, sender_user_id)
                    if reply_message_list:
                        logger.info(f"回复列表：{reply_message_list}")
                        if reply_message_list is None:
                            return None
                        return reply_message_list, sender_user_id, -1
                    else:
                        return None


                elif data['message_type'] == 'group' and self.group_message_reply:
                    group_id = data.get('group_id')
                    if not is_image:
                        logger.info(f"收到来自群{group_id}QQ{sender_user_id}的消息：{message}")
                    else:
                        logger.info(f"收到来自群{group_id}QQ{sender_user_id}的图片消息")
                        
                    ''' 对消息中的 at 信息进行处理过滤 '''
                    self.is_at_message = False
                    self.is_at_message,at_matches,message = process_at_message(self.is_cq_code, data)
                    if at_matches:
                        if str(self.bot_qq_id) not in at_matches:
                            logger.debug(f"消息中不是@机器人，已过滤")
                            return None
                    else:
                        if self.at_reply:
                            logger.debug(f"消息中未@机器人，已过滤")
                            return None
       
                    if group_id not in self.group_message_reply_list and not self.group_anyone:
                        return None
                    
                    if self.group_reply_only_to_trusted:
                        if sender_user_id not in self.trust_qq_list:
                            return None
                        
                    if is_command(message):
                        # 此条消息为命令,需要判断执行者是否有权限执行
                        if self.group_cmd_for_trusted_users_only:
                            if sender_user_id not in self.trust_qq_list:
                                logger.info(
                                    f"执行命令者{sender_user_id}未在白名单中，已过滤"
                                )
                                return None
                        logger.info(f"执行命令：{message}")
                    elif not is_reply_message(
                        self.at_reply, self.reply_rate, self.is_at_message
                    ):
                        logger.info(f"未达到消息回复率{self.reply_rate}%，不回复")
                        return None
                    
                    if is_image:
                        if self.enable_multi_modal:
                            message = self.muice_app.image_query(image_url)

                        elif self.enable_ofa_image:
                            message = await self.image_captioning_pipeline.generate_caption(image_url)
                            await self.image_db.insert_data(message, image_url)
                            message = f"<收到图片描述：{message}>"

                    reply_message_list = await self.produce_group_reply(str(message), sender_user_id, group_id)
                    if is_command(message) and '没有这样的命令呢' in reply_message_list:
                        logger.warning("执行的命令不存在")
                        return None
                    logger.info(f"回复列表：{reply_message_list}")
                    if reply_message_list is None:
                        return None
                    return reply_message_list, sender_user_id, group_id
                else:
                    return None
            else:
                return None
        except json.JSONDecodeError:
            logger.error("JSON解析错误")
            return None
        except Exception as e:
            logger.error(f"处理消息时发生错误: {e}")
            logger.error(f"接收到的数据: {json.dumps(data, ensure_ascii=False)}")
            logger.exception(e)
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

        raw_reply = self.muice_app.ask(text=mess, user_qq=sender_user_id, group_id=-1)
        raw_reply = raw_reply.replace('<USERNAME>', self.nickname)
        logger.debug(f"回复消息：{raw_reply}")
        if self.enable_ofa_image:
            similar_image = await self.image_db.find_similar_content(raw_reply)
            if similar_image is not None and similar_image[1] is not None:
                if similar_image[1] > 0.6:
                    logger.info(f"找到相似图片：{similar_image[0]}，相似度为{similar_image[1]}")
                    try:
                        url = similar_image[0].replace('&', '&amp;')
                    except:
                        pass
                    reply_list = [f"[CQ:image,url={url}]"]
                    return reply_list
        if self.muice_app.think:
            thought, result = process_thoughts(raw_reply, output_thoughts=self.muice_app.think)
            reply_list = divide_sentences(result)
            if thought:
                reply_list.insert(0, thought)
        else:
            result = raw_reply
            reply_list = divide_sentences(raw_reply)
        self.muice_app.save_chat_memory(result)
        if voice_message_reply(self.voice_reply_rate):
            logger.info(f"尝试回复语音消息")
            try:
                voice_file = await fish_speech_api(result)
                reply_list = [f'[CQ:record,file=file:///{voice_file}]']
            except Exception as e:
                logger.error(f"回复语音消息失败: {e}")
        return reply_list

    async def produce_group_reply(self, mess, sender_user_id, group_id) -> list | None:
        """ 回复消息群聊 """
        # msg_raw用来判断是否为命令
        msg_raw = str(mess.strip())
        if not str(mess).strip():
            if self.is_at_message:
                mess="在吗"#待定，中文语境中单at含义与在吗相似
            else:
                return []
            
        '''检测是否匹配前缀'''
        for prefix in self.nonreply_prefix:
            if str(mess).startswith(prefix):
                return []
        if str(msg_raw).startswith("/"):
            # 此处在ask之前,需要手动设置user_id(实际为记忆路径)用于/reset
            self.muice_app.user_id = f"group_{group_id}"
            reply = self.command.run(msg_raw)
            reply_list = divide_sentences(reply)
            return reply_list

        raw_reply = self.muice_app.ask(text=mess, user_qq=sender_user_id, group_id=group_id)
        raw_reply = raw_reply.replace('<USERNAME>', self.nickname)
        logger.info(f"回复消息：{raw_reply}")
        if self.enable_ofa_image:
            similar_image = await self.image_db.find_similar_content(raw_reply)
            if similar_image is not None and similar_image[1] is not None:
                if similar_image[1] > 0.6:
                    logger.info(f"找到相似图片：{similar_image[0]}，相似度为{similar_image[1]}")
                    try:
                        url = similar_image[0].replace('&', '&amp;')
                    except:
                        pass
                    reply_list = [f"[CQ:image,url={url}]"]
                    return reply_list
        if self.muice_app.think:
            thought, result = process_thoughts(raw_reply, output_thoughts=self.muice_app.think)
            reply_list = divide_sentences(result)
            if thought:
                reply_list.insert(0, thought)
        else:
            result = raw_reply
            reply_list = divide_sentences(raw_reply)
        self.muice_app.save_chat_memory(result)
        if voice_message_reply(self.voice_reply_rate):
            logger.info(f"尝试回复语音消息")
            try:
                voice_file = await fish_speech_api(result)
                reply_list = [f'[CQ:record,file=file:///{voice_file}]']
            except Exception as e:
                logger.error(f"回复语音消息失败: {e}")
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
                mess = self.muice_app.ask(topic, key, -1)
                reply = await build_reply_json(mess, key)
                await self.websocket.send_text(reply)

    def run(self):
        logger.info("尝试与适配器建立WebSocket连接...")
        logger.info(f"WebSocket运行地址：http://127.0.0.1:{self.websocket_port}")
        uvicorn.run(self.app, host="127.0.0.1", port=self.websocket_port, log_level="warning")


if __name__ == '__main__':
    logger.warning("用户请勿直接运行此文件，请使用main.py运行")
    Muice_app = None
    ws = QQBot(Muice_app)
    ws.run()