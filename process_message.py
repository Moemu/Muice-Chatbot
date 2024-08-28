import json
import logging
from Tools import configs_tool
from Tools import divide_sentences
from command import Command


class process_message:
    def __init__(self, muice):
        self.muice = muice

        self.configs_tool = configs_tool()
        self.group_message_reply_list = self.configs_tool.get('Trust_QQ_Group_list')
        self.trust_qq_list = self.configs_tool.get('Trust_QQ_list')
        self.group_message_reply = self.configs_tool.get('Group_Message_Reply')
        self.group_reply_only_to_trusted = self.configs_tool.get('Group_Message_Reply_Only_To_Trusted')
        self.is_onebot_plugin = self.configs_tool.get('Is_OneBot_Plugin')
        self.command_prefixes = self.configs_tool.get('Command_Prefixes')
        self.no_reply_prefixes = self.configs_tool.get('No_Reply_Prefixes')

        self.command = Command(muice)
        self.command.load_default_command()

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

        return None

    async def handle_group_message(self, data):
        group_id = data.get('group_id')
        sender_user_id = data.get('sender', {}).get('user_id')
        message = ' '.join([item['data']['text'] for item in data['message'] if item['type'] == 'text'])

        if group_id in self.group_message_reply_list:
            logging.info(f"收到群{group_id}QQ{sender_user_id}的消息：{message}")

            if self.group_reply_only_to_trusted:
                if sender_user_id in self.trust_qq_list:
                    reply_message_list = await self.produce_group_reply(message, sender_user_id, group_id)
                    logging.debug(f"回复list{reply_message_list}")
                    return {"json_list": reply_message_list, "sender_user_id": sender_user_id, "group_id": group_id}
                else:
                    return None
            else:
                reply_message_list = await self.produce_group_reply(message, sender_user_id, group_id)
                logging.debug(f"回复list{reply_message_list}")
                return {"json_list": reply_message_list, "sender_user_id": sender_user_id, "group_id": group_id}

        return None

    async def handle_private_message(self, data):
        sender_user_id = data.get('sender', {}).get('user_id')
        # 解析消息文本
        if self.is_onebot_plugin:
            message = data['message']

        else:
            if not isinstance(data['message'], list):
                logging.error("消息格式错误: data['message'] 不是列表")
                logging.error(f"接收到的数据: {json.dumps(data, ensure_ascii=False, indent=4)}")
                return None
            message = ' '.join([item['data']['text'] for item in data['message'] if item['type'] == 'text'])

        if not message:
            return None

        logging.info(f"收到QQ{sender_user_id}的消息：{message}")
        # 分类处理
        if sender_user_id in self.trust_qq_list:
            if any(message.startswith(prefix) for prefix in self.no_reply_prefixes):
                return None
            elif any(message.startswith(prefix) for prefix in self.command_prefixes):
                # 运行指令
                space_index = message.find(' ')
                if space_index == -1:
                    return None
                else:
                    command = message[:space_index][1:]
                return self.command.run(command,data)
            else:
                reply_message_list = await self.produce_reply(message, sender_user_id)
                logging.debug(f"回复list{reply_message_list}")
                return {"message_list": reply_message_list, "sender_user_id": sender_user_id, "group_id": -1}
        return None

    async def handle_meta_event(self, data):
        if 'meta_event_type' in data:
            if data['meta_event_type'] == 'lifecycle':
                if data['sub_type'] == 'connect':
                    logging.info("已链接")
            elif data['meta_event_type'] == 'heartbeat':
                pass
        return None

    async def produce_reply(self, mess, sender_user_id):
        """ 调用模型 回复消息 """
        reply = self.muice.ask(text=mess, user_qq=sender_user_id, group_id=-1)
        logging.info(f"回复消息：{reply}")
        reply_list = divide_sentences(reply)
        self.muice.finish_ask(reply_list)
        return reply_list

    async def produce_group_reply(self, mess, sender_user_id, group_id):
        """ 回复消息群聊 """
        if not str(mess).strip():
            return None
        if str(mess).startswith('/'):
            reply = self.command.run(mess)
            return reply
        else:
            reply = self.muice.ask(text=mess, user_qq=sender_user_id, group_id=group_id)
            logging.info(f"回复消息：{reply}")
            reply_list = divide_sentences(reply)
            self.muice.finish_ask(reply_list)
            return reply_list
