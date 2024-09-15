import logging

import uvicorn
from fastapi import FastAPI, WebSocket
import asyncio
from process_message import process_message
from Tools import build_msg_reply_json


async def send_message(websocket, data):
    if data is None:
        return None
    group_id = data.get('group_id', -1)
    reply_list = data.get('message_list', [])
    if not reply_list:
        return None
    reply_type = data.get('type', 'msg')
    logging.debug(f'发送列表:{reply_list}')
    if reply_list is None:
        return None
    if reply_type == 'msg':
        if group_id == -1:
            qq_id = data['sender_user_id']
            is_group_or_private = "send_private_msg"
        else:
            qq_id = data['group_id']
            is_group_or_private = "send_group_msg"
        for key in reply_list:
            message_json = await build_msg_reply_json(key, qq_id, is_group_or_private)
            logging.info(f'发送消息{key}')
            await websocket.send_text(message_json)
    # 在此拓展type类型发送
    return None


class BotWebSocket:
    def __init__(self, configs_tool):
        """获取配置"""
        self.configs_tool = configs_tool
        self.ws_host = self.configs_tool.get('Ws_Host')
        self.ws_port = self.configs_tool.get('Ws_Port')

        self.process_message_func = None
        self.app = FastAPI()
        self.received_messages_queue = asyncio.Queue()
        self.messages_to_send_queue = asyncio.Queue()

        @self.app.websocket("/ws/api")
        async def websocket_endpoint(websocket: WebSocket):

            await websocket.accept()
            asyncio.create_task(self.reply_messages())
            asyncio.create_task(self.create_messages(websocket))
            # 这里 不要 await!!

            try:
                async for message in websocket.iter_text():
                    await self.received_messages_queue.put(message)
                    print(f"Received: {message}")
            except Exception as e:
                print(f"WebSocket disconnected: {e}")

    def initialize_model(self, chat_model, other):
        """在此传入模型"""
        self.process_message_func = process_message(chat_model)
        pass

    async def reply_messages(self):
        """从消息队列取出消息传入处理,处理后加入发送队列"""
        while True:
            try:
                print("reply_messages")
                data = await self.received_messages_queue.get()
                # data格式如下:{"group_id": -1, "message_list": ["1", "2"], "sender_user_id": 114514}
                processed_message = await self.process_message_func.reply_message(data)
                if processed_message is not None:
                    await self.messages_to_send_queue.put(processed_message)

                self.received_messages_queue.task_done()
            except:
                continue

    async def create_messages(self, websocket: WebSocket):
        """从发送队列取出消息发送"""
        while True:
            try:
                print("send_messages")
                data = await self.messages_to_send_queue.get()
                logging.debug(f'data:{data}')

                await send_message(websocket, data)  # 分类发送消息
                self.messages_to_send_queue.task_done()
            except:
                continue

    def run(self):
        uvicorn.run(self.app, host=self.ws_host, port=self.ws_port)


if __name__ == '__main__':
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)
    logging.warning("用户请勿直接运行此文件，请使用main.py运行")
    logging.warning("用户请勿直接运行此文件，请使用main.py运行")
    logging.warning("用户请勿直接运行此文件，请使用main.py运行")
    muice = None
    ws = BotWebSocket(muice)
    ws.run()
