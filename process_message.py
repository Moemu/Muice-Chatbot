import json
import logging
import time

from Tools import divide_sentences
from command import Command
from process_memory import *


class process_message:
    def __init__(self, model, configs_tool):
        self.model = model

        self.configs_tool = configs_tool

        self.trust_qq_list = self.configs_tool.get('Trust_QQ_list')

        self.is_onebot_plugin = self.configs_tool.get('Is_OneBot_Plugin')
        self.command_prefixes = self.configs_tool.get('Command_Prefixes')
        self.no_reply_prefixes = self.configs_tool.get('No_Reply_Prefixes')
        self.memory_prefix = self.configs_tool.get('Memory_Prefix')

        self.group_message_reply = self.configs_tool.get('Group_Message_Reply')
        if self.group_message_reply:
            self.group_message_reply_list = self.configs_tool.get('Trust_QQ_Group_list')
            self.group_reply_only_to_trusted = self.configs_tool.get('Group_Message_Reply_Only_to_Trusted')
        else:
            self.group_message_reply_list = []
            self.group_reply_only_to_trusted = True

        self.auto_create_topic = self.configs_tool.get('AutoCreateTopic')
        if self.auto_create_topic:
            self.time_dict = {qq_id: time.time() for qq_id in self.trust_qq_list}

        self.model_doc = self.model.doc()
        # self.model_ask_test = self.model.ask()
        self.is_agent = self.model_doc["is_Agent"]

        self.command = Command(model, self.configs_tool)  # 修改

    async def reply_message(self, data):
        data = json.loads(data)
        logging.debug(f"收到{data}")

        if 'post_type' in data:
            if data['post_type'] == 'meta_event':
                return await self.handle_meta_event(data)
            elif data['post_type'] == 'message':
                logging.debug(f"收到消息")
                if data['message_type'] == 'private':
                    return await self.handle_private_message(data)
                elif data['message_type'] == 'group' and self.group_message_reply:
                    return await self.handle_group_message(data)
                # 用不了 根本是没用的

        return None

    async def handle_group_message(self, data):
        group_id = data.get('group_id')
        sender_user_id = data.get('sender', {}).get('user_id')
        # 解析消息文本
        if self.is_onebot_plugin:
            message = data['message'].replace('\n', ' ')

        else:
            if not isinstance(data['message'], list):
                logging.error("消息格式错误: data['message'] 不是列表")
                logging.error(f"接收到的数据: {json.dumps(data, ensure_ascii=False, indent=4)}")
                return None
            message = ' '.join(
                [item['data']['text'].replace('\n', ' ') for item in data['message'] if item['type'] == 'text'])

        if not message:
            return None

        logging.info(f"收到QQ群{group_id}用户{sender_user_id}的消息：{message}")
        if group_id in self.group_message_reply_list:
            save_memory("group_" + str(group_id), str(sender_user_id) + ":" + message)
            # 储存记忆(可能储存指令等,所以逻辑要改)
        # 分类处理
        if sender_user_id in self.trust_qq_list and group_id in self.group_message_reply_list:
            # 帮帮我吧, 逻辑不想写啦
            if any(message.startswith(prefix) for prefix in self.no_reply_prefixes):
                return None

            for prefix in self.command_prefixes:
                if message.startswith(prefix):
                    if len(prefix) > 0:
                        message_without_prefix = message[len(prefix):]
                        space_index = message_without_prefix.find(' ')
                        if space_index == -1:
                            command = message_without_prefix
                        else:
                            command = message_without_prefix[:space_index]

                        reply = self.command.run(command, data, message)
                        if reply:
                            reply_message_list = reply["data"]
                            reply_type = reply["type"]
                            return {"message_list": reply_message_list, "sender_user_id": sender_user_id,
                                    "group_id": group_id,
                                    "type": reply_type}

            else:
                msg_time = data["time"]
                reply_message_list = await self.produce_group_reply(message, group_id, msg_time)
                logging.debug(f"回复list{reply_message_list}")
                return {"message_list": reply_message_list, "sender_user_id": sender_user_id, "group_id": group_id,
                        "type": "msg"}
        return None

    async def handle_private_message(self, data):
        sender_user_id = data.get('sender', {}).get('user_id')
        # 解析消息文本
        if self.is_onebot_plugin:
            message = data['message'].replace('\n', ' ')

        else:
            if not isinstance(data['message'], list):
                logging.error("消息格式错误: data['message'] 不是列表")
                logging.error(f"接收到的数据: {json.dumps(data, ensure_ascii=False, indent=4)}")
                return None
            message = ' '.join(
                [item['data']['text'].replace('\n', ' ') for item in data['message'] if item['type'] == 'text'])

        if not message:
            return None

        logging.info(f"收到QQ{sender_user_id}的消息：{message}")
        # 分类处理
        if sender_user_id in self.trust_qq_list:
            if any(message.startswith(prefix) for prefix in self.no_reply_prefixes):
                return None

            for prefix in self.command_prefixes:
                if message.startswith(prefix):
                    if len(prefix) > 0:
                        message_without_prefix = message[len(prefix):]
                        space_index = message_without_prefix.find(' ')
                        if space_index == -1:
                            command = message_without_prefix
                        else:
                            command = message_without_prefix[:space_index]

                        reply = self.command.run(command, data, message)
                        if reply:
                            reply_message_list = reply["data"]
                            reply_type = reply["type"]
                            return {"message_list": reply_message_list, "sender_user_id": sender_user_id,
                                    "group_id": -1,
                                    "type": reply_type}

            else:
                msg_time = data["time"]
                reply_message_list = await self.produce_reply(message, sender_user_id, msg_time)
                logging.debug(f"回复list{reply_message_list}")
                return {"message_list": reply_message_list, "sender_user_id": sender_user_id, "group_id": -1,
                        "type": "msg"}
        return None

    async def produce_reply(self, message, sender_user_id, msg_time):
        """ 调用模型 回复消息 """
        if self.is_agent:
            # 啊 等模型出来了再补吧
            return None
        else:
            memory = build_memory_list("private_" + str(sender_user_id))
            memory = self.memory_prefix + memory
            reply = self.model.ask(message, memory)  # 得到回复文本
            save_memory("private_" + str(sender_user_id), str(sender_user_id) + ":" + message)
            save_memory("private_" + str(sender_user_id), "-1:" + reply)
        logging.info(f"回复{sender_user_id}消息：{reply}")
        reply_list = divide_sentences(reply)
        return reply_list

    # 以下内容 没写呢 看啥看 看到了就帮我写!
    async def handle_meta_event(self, data):
        # 啊 没写呢 还准备处理心跳的
        if 'meta_event_type' in data:
            if data['meta_event_type'] == 'lifecycle':
                if data['sub_type'] == 'connect':
                    logging.info("已链接")
            elif data['meta_event_type'] == 'heartbeat':
                pass
        return None

    async def produce_group_reply(self, message, group_id, msg_time):
        """ 调用模型 回复消息 """
        if self.is_agent:
            # 啊 等模型出来了再补吧
            return None
        else:
            memory = build_memory_list("group_" + str(group_id))
            memory = self.memory_prefix + memory
            reply = self.model.ask(message, memory)  # 得到回复文本
            save_memory("group_" + str(group_id), "-1:" + reply)
        logging.info(f"回复{group_id}消息：{reply}")
        reply_list = divide_sentences(reply)
        return reply_list

    async def auto_create_topic(self):
        result = []
        for key, value in self.time_dict.items():
            topic = self.command.create_a_new_topic(value)
            if topic is None:
                continue
            else:
                self.time_dict[key] = time.time()
                msg = self.model.ask(topic, [])
                result.append({key: msg})
        return result
