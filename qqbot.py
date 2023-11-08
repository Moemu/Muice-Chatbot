from pycqBot.cqHttpApi import cqHttpApi, cqLog
from pycqBot.data import Message
from Muice import Muice
from command import Command
import logging
import time

def qqbot(Muice: Muice, Trust_QQ_list: list, AutoCreateTopic: False):
    command = Command(Muice)
    command.load_default_command()
    cqLog(level=logging.INFO, logPath='./qqbot/cqLogs')
    cqapi = cqHttpApi(download_path='./qqbot/download')

    def on_private_msg(message: Message):
        user_qq = message.sender.id
        if 'CQ' in message.message:
            return
        else:
            is_command,result = command.run(message.message)
            if is_command and result != '':
                reply = result
            elif is_command and result == '':
                reply = "操作已完成"
            else:
                reply = Muice.ask(message.message,user_qq)
        try:
            if type(reply) == list:           
                for st in reply:
                    if st == '' or st == ' ':
                        continue
                    if not is_command:
                        time.sleep(len(st)*0.8)
                    message.sender.send_message(st)
                    logging.info(f'发送信息: {st}')
                    time.sleep(3)
            elif type(reply) == str and not reply in ['',' ']:
                if not is_command:
                    time.sleep(len(st)*0.8)
                message.sender.send_message(reply)
                logging.info(f'发送信息: {reply}')
            else:
                logging.error(f'不支持的回复类型: {reply}')
            Muice.finish_ask(reply,is_command)
        except Exception as e:
            logging.error(e)

    def CreateANewChat(args):
        '''
        主动发起对话
        '''
        topic = Muice.CreateANewTopic()
        reply = Muice.ask(topic,Trust_QQ_list[0])
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