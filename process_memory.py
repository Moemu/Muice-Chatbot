import json
import logging
import os


async def get_pr_memory_old(user_id, time):
    try:
        with open(f'./memory/{user_id}.json', 'r', encoding='utf-8') as f:
            data = f.readlines()
            logging.debug(f'Muice.py->get_recent_chat_memory->{user_id}')
            return json.loads(data[-2])['history']

    except FileNotFoundError as e:
        logging.error(f"文件未找到: {e}")
        return []
    except Exception as e:
        logging.error(f"发生了一个错误: {e}")
        return []


def build_memory_list(file_path):
    if not os.path.exists(f'./memory/{file_path}.json'):
        logging.error(f"文件未找到: {file_path}")
        logging.info(f"创建文件: {file_path}")
        with open(f'./memory/{file_path}.json', 'w', encoding='utf-8') as file:
            file.write('')
    bot_msg_num = 0
    memory_list = []
    one_turn_reply_list = []
    last_user_id = -1
    reply = ""
    try:
        with open(f'./memory/{file_path}.json', 'r', encoding='utf-8', ) as file:
            file.seek(0, 2)  # 移动到文件末尾
            position = file.tell()  # 获取当前位置
            while position > 0:
                file.seek(position - 1, 0)  # 向前移动一位
                position = file.tell()
                while position > 0 and file.read(1) != '\n':  # 找到换行符
                    position -= 1
                    file.seek(position, 0)
                if position > 0:
                    data = file.readline().strip()
                    if ":" not in data:
                        logging.warning(f"无效的数据格式: {data}")
                        continue
                    user, message = data.split(":", 1)
                    if (last_user_id == -1 and user == -1) or (last_user_id != -1 and user != -1):
                        reply = message + reply
                    else:
                        last_user_id = user
                        if user == -1:
                            bot_msg_num += 1
                            if bot_msg_num >= 6:
                                logging.debug(f'构建记忆列表完成{memory_list}')
                                return memory_list
                            memory_list = one_turn_reply_list + memory_list
                            one_turn_reply_list = []
                        one_turn_reply_list = [reply] + one_turn_reply_list
                        reply = ""
        logging.debug(f'构建记忆列表完成{memory_list}')
        return memory_list
    except Exception as e:
        logging.error(f"发生了一个错误: {e}")
        return []


def save_memory(file_path, data):
    logging.debug(f'保存记忆列表完成{data}')
    try:
        with open(f'./memory/{file_path}.json', 'a', encoding='utf-8') as file:
            file.write(data + '\n')
    except Exception as e:
        logging.error(f"发生了一个错误: {e}")
