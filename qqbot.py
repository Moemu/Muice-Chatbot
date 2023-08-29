from pycqBot.cqHttpApi import cqHttpApi, cqLog
from pycqBot.data import Message
from Muice import Muice
import logging
import time

def qqbot(Muice: Muice, Trust_QQ_list: list, AutoCreateTopic: False):
    cqLog(level=logging.INFO, logPath='./qqbot/cqLogs')
    cqapi = cqHttpApi(download_path='./qqbot/download')

    def on_private_msg(message: Message):
        # user_info = message.sender.get_stranger_info()
        # nickname = user_info['data']['nickname']
        # sender = message.sender
        # message = message.message
        # prompt = f'{nickname}: {message}'  
        if 'CQ' in message.message:
            return
        else:
            reply = Muice.ask(message.message)
        try:           
            for st in reply:
                if st == '' or st == ' ':
                    continue
                message.sender.send_message(st)
                logging.info(f'发送信息: {st}')
                time.sleep(3)
            Muice.finish_ask(reply)
        except Exception as e:
            logging.error(e)

    def CreateANewChat(args):
        '''
        主动发起对话
        '''
        topic = Muice.CreateANewTopic()
        reply = Muice.ask(topic)
        if reply != '':
            for st in reply:
                time.sleep(3)
                if st == '' or st == ' ':
                    continue
                cqapi.send_private_msg(Trust_QQ_list[0],message=st)
                logging.info(f'发送信息: {st}')

    bot = cqapi.create_bot(
        group_id_list=[0],
        user_id_list=Trust_QQ_list
    )
    bot.on_private_msg = on_private_msg

    if AutoCreateTopic:
        bot.timing(CreateANewChat,"CreateANewTopic",{"timeSleep":60})
    bot.start(go_cqhttp_path='./qqbot/')