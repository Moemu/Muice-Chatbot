import json
import logging
import os
import random
import time


class Muice:
    """
    Muice交互类
    """

    def __init__(self, model, read_memory_from_file: bool = True, known_topic_probability: float = 0.003,
                 time_topic_probability: float = 0.75):
        self.reply = None
        self.user_text = None
        self.history = None
        self.user_id = None
        self.model = model
        self.read_memory_from_file = read_memory_from_file
        self.known_topic_probability = known_topic_probability
        self.time_topic_probability = time_topic_probability
        self.known_topic = ['（分享一下你的一些想法）', '（创造一个新话题）']
        self.time_topic = {'07': '（发起一个早晨问候）', '12': '（发起一个中午问候）', '18': '（发起一个傍晚问候）',
                           '00': '（发起一个临睡问候）'}
        self.time_topics = self.time_topic.copy()

    def ask(self, text: str, user_qq: int, group_id: int) -> str:
        """发送信息"""
        if group_id == -1:
            self.user_id = str(user_qq)
        else:
            self.user_id = "group_" + str(group_id)

        if self.read_memory_from_file:
            self.history = self.get_recent_chat_memory()
        else:
            self.history = []

        self.user_text = text
        start_time = time.time()
        self.reply = self.model.ask(self.user_text, self.history)
        end_time = time.time()
        logging.info(f'模型调用时长: {end_time - start_time} s')
        return self.reply

    def create_a_new_topic(self, last_time):
        """
        主动发起对话
        """
        current_time = time.strftime("%H:%M", time.localtime())
        time_difference = time.time() - last_time
        if time_difference < 60 * 60:
            return None
        if random.random() < self.time_topic_probability:
            for hour, topic in self.time_topic.items():
                event_time = hour + ':' + str(random.randint(0, 59))
                if event_time == current_time:
                    del self.time_topic[hour]
                    return topic
        if not current_time.split(':')[0] in ['23', '00', '01', '02', '03', '04', '05',
                                              '06'] and random.random() < self.known_topic_probability:
            return random.choice(self.known_topic)
        if len(self.time_topic) <= 3 and not time.strftime("%H", time.localtime()) in self.time_topics.keys():
            self.time_topic = self.time_topics.copy()
        return None

    def finish_ask(self, reply: list):
        """
        结束对话并保存记忆
        """
        logging.debug(f'Muice.py->finish_ask->{reply}')
        reply = "".join(reply)
        self.save_chat_memory(reply)

    def get_recent_chat_memory(self):
        """
        获取最近一条记忆
        """
        if not os.path.isfile(f'./memory/{self.user_id}.json') or self.user_id == None:
            return []
        else:
            try:
                with open(f'./memory/{self.user_id}.json', 'r', encoding='utf-8') as f:
                    data = f.readlines()
                logging.debug(f'Muice.py->get_recent_chat_memory->{self.user_id}')
                if len(data) == 0:
                    return []
                memory = json.loads(data[-1])
                memory['history'].append([memory['prompt'],memory['completion']])
                return memory['history']
            except Exception as e:
                logging.error(f"记忆文件内部发生了一个错误，已更名此文件: {e}")
                if os.path.isfile(f'./memory/{self.user_id}.json.bak'):
                    os.remove(f'./memory/{self.user_id}.json.bak')
                os.rename(f'./memory/{self.user_id}.json', f'./memory/{self.user_id}.json.bak')
                return []

    def save_chat_memory(self, reply: str):
        """
        保存至记忆数据库
        """
        if not os.path.isdir('memory'):
            os.mkdir('memory')
        if not self.user_id:
            return
        with open(f'./memory/{self.user_id}.json', 'a', encoding='utf-8') as f:
            logging.debug(f'保存用户记忆:{self.user_id},{self.history}')
            json.dump({'prompt': self.user_text, 'completion': reply, 'history': self.history}, f, ensure_ascii=False)
            f.write('\n')

    def remove_last_chat_memory(self):
        """
        删除最后一条记忆
        """
        if not os.path.isfile(f'./memory/{self.user_id}.json'):
            return
        with open(f'./memory/{self.user_id}.json', 'r', encoding='utf-8') as f:
            data = f.readlines()
            if len(data) > 1:
                del data[-1]
            else:
                data = []
        with open(f'./memory/{self.user_id}.json', 'w', encoding='utf-8') as f:
            f.writelines(data)

    def refresh(self) -> str:
        """
        刷新对话
        """
        logging.info("Start refresh")
        if not self.user_text:
            return "本雪一句话都没有和你说！你在玩我呢？"
        self.remove_last_chat_memory()
        self.history = self.get_recent_chat_memory()
        logging.debug(f'刷新后历史记录:{self.history}')
        response = self.model.ask(self.user_text, self.history)
        return response
