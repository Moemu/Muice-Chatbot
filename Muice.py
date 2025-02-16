import json
import logging
import os
import random
import time
import re

logger = logging.getLogger('Muice')

class Muice:
    """
    Muice交互类
    """

    def __init__(self, model, memory, configs):
        self.reply = None
        self.user_text = None
        self.history = None
        self.user_id = None
        self.clean_memory = False
        self.model = model
        self.memory = memory
        self.configs = configs

        if self.configs['active']['rate']:
            self.known_topic_probability = self.configs['active']['rate']
        else:
            self.known_topic_probability = 0
        if self.configs['active']['shecdule']['enable']:
            self.time_topic_probability = self.configs['active']['shecdule']['rate']
        else:
            self.time_topic_probability = 0

        self.known_topic = self.configs['active']['active_prompts']
        self.time_topic = self.configs['active']['shecdule']['tasks']
        self.time_topic_backup = self.time_topic.copy()
        self.think = self.configs.get("model", {}).get("think", 0)

    def ask(self, text: str, user_qq: int, group_id: int) -> str:
        """发送信息"""
        logger.info('正在调用模型...')
        if group_id == -1:
            self.user_id = str(user_qq)
        else:
            self.user_id = "group_" + str(group_id)

        history = self.get_recent_chat_memory()
        self.user_text = text

        if self.memory is not None:
            variables = self.memory.search_memory({"input": self.user_text})
            if variables != {"input": ["", ""], "output": ["", ""]}:
                faiss_inputs = variables.get('input', [])
                if faiss_inputs is not None:
                    faiss_outputs = variables.get('output', [])
                    self.history = history[:5] + [[inp, out] for inp, out in zip(faiss_inputs, faiss_outputs) if inp and out] # 至少保留最近5条对话避免丢失上下文信息
            else:
                self.history = history
        else:
            self.history = history

        # 列表去重
        self.history = [list(t) for t in set(tuple(i) for i in self.history)]

        start_time = time.time()
        logger.debug(f'模型调用参数：Prompt: {self.user_text}, History: {self.history}')
        self.reply:str = self.model.ask(self.user_text, self.history).strip()
        end_time = time.time()
        logger.info(f'模型调用时长: {end_time - start_time} s')
        return self.reply

    def create_a_new_topic(self, last_time):
        """
        主动发起对话
        args:
            last_time: 上次对话时间
        """
        current_time = time.strftime("%H:%M", time.localtime())
        current_hour = time.strftime("%H", time.localtime())
        time_difference = time.time() - last_time

        # 如果距离上次对话时间小于30分钟，则不主动发起对话
        if time_difference < 30 * 60:
            return None
        
        # 尝试生成日常定时Prompt
        if random.random() < self.time_topic_probability:
            for index,task in enumerate(self.time_topic):
                event_time = str(task['hour']) + ':' + str(random.randint(0, 59))
                if event_time == current_time:
                    del self.time_topic[index]
                    return task['prompt']

        # 尝试生成不定时Prompt
        if (not self.configs['active']['enable']) or not (current_hour in ['23', '00', '01', '02', '03', '04', '05', '06']):
            if random.random() < self.known_topic_probability:
                return random.choice(self.known_topic)
        
        # 日常定时Prompt使用后重置
        if len(self.time_topic) < len(self.time_topic_backup) and time_difference > 60 * 60:
            self.time_topic = self.time_topic_backup.copy()
        
        return None

    def get_recent_chat_memory(self):
        """
        获取最近一条记忆
        """
        if self.clean_memory:
            self.clean_memory = False
            return []
        if not os.path.isfile(f'./memory/{self.user_id}.json') or not self.user_id:
            return []
        try:
            with open(f'./memory/{self.user_id}.json', 'r', encoding='utf-8') as f:
                data = f.readlines()
            if len(data) == 0:
                return []
            memory = json.loads(data[-1])
            memory['history'].append([memory['prompt'],memory['completion']])
            return memory['history']
        except Exception as e:
            logger.warning(f"记忆文件内部发生了一个错误，已更名此文件: {e}")
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
        image_pattern = r"收到图片描述：([^)]+)"
        image_matches = re.search(image_pattern,self.user_text)
        if image_matches:
            image_caption = image_matches.group(1)
            with open(f'./memory/{self.user_id}.json', 'a', encoding='utf-8') as f:
                logger.debug(f'保存用户{self.user_id}记忆：{self.history[-1]}')
                json.dump({'prompt': image_caption, 'completion': reply, 'history': self.history}, f, ensure_ascii=False)
                f.write('\n')
            return
        with open(f'./memory/{self.user_id}.json', 'a', encoding='utf-8') as f:
            json.dump({'prompt': self.user_text, 'completion': reply, 'history': self.history}, f, ensure_ascii=False)
            f.write('\n')
        if self.memory is not None:
            self.memory.insert_memory({"input": self.user_text}, {"output": reply})
        logger.debug(f'保存用户{self.user_id}记忆：[{self.user_text}, {reply}]')

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
        logger.info("开始刷新对话")
        if not self.user_text:
            return "我一句话都没有和你说！你在玩我呢？"
        self.remove_last_chat_memory()
        self.history = self.get_recent_chat_memory()
        logger.debug(f'刷新后历史记录：{self.history}')
        response = self.model.ask(self.user_text, self.history)
        return response
