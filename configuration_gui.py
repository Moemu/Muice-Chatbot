import os
import time
import json
from prompt_toolkit.shortcuts import yes_no_dialog
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.shortcuts import checkboxlist_dialog
from prompt_toolkit.shortcuts import message_dialog

config_infomation = [
    {
        "key": "model_loader",
        "name": "模型加载器",
        "type": "str",
        "description": "模型加载器，决定模型的加载方法。",
        "recommend": "api, llmtuner, rwkv-api, transformers",
        "range": ("api", "llmtuner", "rwkv-api", "transformers")
    },
    {
        "key": "model_name_or_path",
        "name": "LLM模型名称或路径",
        "type": "str",
        "description": "LLM模型名称或路径。",
        "recommend": None
    },
    {
        "key": "adapter_name_or_path",
        "name": "微调模型名称或路径",
        "type": "str",
        "description": "微调模型名称或路径。",
        "recommend": "./model/Muice"
    },
    {
        "key": "enable_ofa_image",
        "name": "是否启用OFA图像识别",
        "type": "bool",
        "description": "是否启用OFA图像识别和发送图片。",
        "recommend": "True"
    },
    {
        "key": "ofa_image_model_name_or_path",
        "name": "OFA图像识别模型名称或路径",
        "type": "str",
        "description": "OFA图像识别模型名称或路径。",
        "recommend": "./model/ofa_image"
    },
    {
        "key": "audio_name_or_path",
        "name": "音频模型名称或路径",
        "type": "str",
        "description": "音频模型名称或路径(仅在实时推理时使用)。",
        "recommend": "./model/SenseVoice"
    },
    {
        "key": "read_memory_from_file",
        "name": "是否存储短期记忆",
        "type": "bool",
        "description": "是否向本地文件存储短期记忆。",
        "recommend": "True"
    },
    {
        "key": "AutoCreateTopic",
        "name": "是否自动创建话题",
        "type": "bool",
        "description": "是否自动创建话题。",
        "recommend": "False"
    },
    {
        "key": "known_topic_probability",
        "name": "已知话题概率",
        "type": "float",
        "description": "已知话题概率。",
        "recommend": "0.003",
        "range": (0, 1),
        "hidden": True
    },
    {
        "key": "time_topic_probability",
        "name": "时间话题概率",
        "type": "float",
        "description": "每一时刻发动话题的概率。",
        "recommend": "0.75",
        "range": (0, 1),
        "hidden": True
    },
    {
        "key": "Trust_QQ_list",
        "name": "可信QQ列表",
        "type": "list",
        "description": "用于配置可信的QQ号，只有这些号码的消息才会被处理。(使用;分隔)",
        "recommend": None
    },
    {
        "key": "port",
        "name": "端口号",
        "type": "int",
        "description": "用于配置WebSocket服务运行的端口号。",
        "recommend": "21050",
        "range": (1024, 65535)
    },
    {
        "key": "Group_Message_Reply",
        "name": "群消息回复",
        "type": "bool",
        "description": "是否开启群消息回复。",
        "recommend": "True"
    },
    {
        "key": "Trust_QQ_Group_list",
        "name": "可信群列表",
        "type": "list",
        "description": "用于配置可信的群号，只有这些群的消息才会被处理。(使用;分隔)",
        "recommend": None
    },
    {
        "key": "Group_Message_Reply_Only_To_Trusted",
        "name": "仅回复可信群消息",
        "type": "bool",
        "description": "是否仅回复可信群消息。",
        "recommend": "True"
    },
    {
        "key": "Is_CQ_Code",
        "name": "是否启用CQ码处理信息",
        "type": "bool",
        "description": "是否启用CQ码处理信息(部分适配器较老，未适配新消息段)。",
        "recommend": "False"
    },
    {
        "key": "bot_qq_id",
        "name": "机器人QQ号",
        "type": "int",
        "description": "用于配置机器人的QQ号。",
        "recommend": None
    },
    {
        "key": "Reply_Rate",
        "name": "消息回复概率",
        "type": "int",
        "description": "机器人回复消息的概率。",
        "recommend": "50",
        "range": (0, 100)
    },
    {
        "key": "At_Reply",
        "name": "艾特回复",
        "type": "bool",
        "description": "是否仅开启艾特回复。",
        "recommend": "False"
    },
    {
        "key": "NonReply_Prefix",
        "name": "非回复消息前缀",
        "type": "list",
        "description": "用于配置机器人的非回复消息前缀符号。(使用;分隔)",
        "recommend": "#;!"
    },
    {
        "key": "Voice_Reply_Rate",
        "name": "语音回复概率",
        "type": "int",
        "description": "机器人回复语音的概率。(设置为0则不回复语音)",
        "recommend": "50",
        "range": (0, 100)
    },
    {
        "key": "Group_Ignore_Cmd_Not_Found",
        "name": "群消息忽略命令未找到错误",
        "type": "bool",
        "description": "是否忽略用户在群内使用/找不到命令的提示。",
        "recommend": "True"
    },
    {
        "key": "Group_Cmd_For_Trusted_Users_Only",
        "name": "仅允许可信用户在群使用命令",
        "type": "bool",
        "description": "若开启，机器人不会理会可信列表之外的人使用命令。",
        "recommend": "True"
    }
]

# 设置配置默认值
model_loader = "llmtuner"
model_name_or_path = "./model/model"
adapter_name_or_path = "./model/Muice"
enable_ofa_image = False
ofa_image_model_name_or_path = "./model/ofa_image"
audio_name_or_path = "./model/SenseVoice"
read_memory_from_file = True
AutoCreateTopic = False
known_topic_probability = 0.003
time_topic_probability = 0.75
Trust_QQ_list = []
port = 21050
Group_Message_Reply = True
Trust_QQ_Group_list = []
Group_Message_Reply_Only_To_Trusted = True
Is_CQ_Code = False
bot_qq_id = None
Reply_Rate = 50
At_Reply = False
NonReply_Prefix = ["#"]
Voice_Reply_Rate = 50
Group_Cmd_For_Trusted_Users_Only = True
Group_Ignore_Cmd_Not_Found = True

def str_messagebox(index):
    """
    配置字符串类型的config。
    """
    key = config_infomation[index]["key"]
    name = config_infomation[index]["name"]
    description = config_infomation[index]["description"]
    recommend = config_infomation[index]["recommend"]
    value = globals()[key]
    if value is None:
        value = ""
    message = f"{description}\n默认值：{value}\n推荐值：{recommend}\n"
    result = input_dialog(
        title=f"{name}", text=message,
    ).run()
    if result is None:
        return False
    if result == '':
        result = globals()[key]
    try:
        range_ = config_infomation[index]["range"]
        if range_ is not None:
            if result not in range_:
                print("输入值不在范围内")
                return False
    except:
        pass
    globals()[key] = result
    return True

def bool_messagebox(index):
    """
    配置布尔类型的config。
    """
    key = config_infomation[index]["key"]
    name = config_infomation[index]["name"]
    description = config_infomation[index]["description"]
    recommend = config_infomation[index]["recommend"]
    value = globals()[key]
    message = f"{description}\n默认值：{value}\n推荐值：{recommend}\n"
    result = radiolist_dialog(
        values=[("True", 'True'), ("False", 'False')],
        title=f"{name}", text=message,
    ).run()
    if result is None:
        return False
    if result == '':
        result = globals()[key]
    if result == 'True':
        globals()[key] = True
    else:
        globals()[key] = False
    return True

def list_messagebox(index):
    """
    配置列表类型的config。
    """
    key = config_infomation[index]["key"]
    name = config_infomation[index]["name"]
    description = config_infomation[index]["description"]
    recommend = config_infomation[index]["recommend"]
    value = globals()[key]
    if value is None:
        value = ""
    message = f"{description}\n默认值：{value}\n推荐值：{recommend}\n"
    result = input_dialog(
        title=f"{name}", text=message,
    ).run()
    if result is None:
        if key != "NonReply_Prefix":
            return False
    if result == '':
        result = globals()[key]
    if isinstance(result, list):
        return True
    globals()[key] = result.split(";")
    return True

def float_messagebox(index):
    """
    配置浮点类型的config。
    """
    key = config_infomation[index]["key"]
    name = config_infomation[index]["name"]
    description = config_infomation[index]["description"]
    recommend = config_infomation[index]["recommend"]
    value = globals()[key]
    message = f"{description}\n默认值：{value}\n推荐值：{recommend}\n"
    result = input_dialog(
        title=f"{name}", text=message,
    ).run()
    if result is None:
        return False
    if result == '':
        result = globals()[key]
    try:
        range_ = config_infomation[index]["range"]
        if range_ is not None:
            if float(result) not in range(range_):
                print("输入值不在范围内")
                return False
    except:
        pass
    globals()[key] = float(result)
    return True

def int_messagebox(index):
    """
    配置整数类型的config。
    """
    key = config_infomation[index]["key"]
    name = config_infomation[index]["name"]
    description = config_infomation[index]["description"]
    recommend = config_infomation[index]["recommend"]
    value = globals()[key]
    message = f"{description}\n默认值：{value}\n推荐值：{recommend}\n"
    result = input_dialog(
        title=f"{name}", text=message,
    ).run()
    if result is None:
        return False
    if result == '':
        result = globals()[key]
    try:
        range_ = config_infomation[index]["range"]
        if range_ is not None:
            if int(result) not in range(range_):
                print("输入值不在范围内")
                return False
    except:
        pass
    if result is None:
        result = 0
    globals()[key] = int(result)
    return True

def set_config(keys):
    """
    设置配置。
    """
    if keys == []:
        for index in range(len(config_infomation)):
            if config_infomation[index]["type"] == "str":
                while not str_messagebox(index):
                    print("输入值不符合要求，请重新输入")
                    time.sleep(3)
            elif config_infomation[index]["type"] == "bool":
                while not bool_messagebox(index):
                    print("输入值不符合要求，请重新输入")
                    time.sleep(3)
            elif config_infomation[index]["type"] == "list":
                while not list_messagebox(index):
                    print("输入值不符合要求，请重新输入")
                    time.sleep(3)
            elif config_infomation[index]["type"] == "float":
                while not float_messagebox(index):
                    print("输入值不符合要求，请重新输入")
                    time.sleep(3)
            elif config_infomation[index]["type"] == "int":
                while not int_messagebox(index):
                    print("输入值不符合要求，请重新输入")
                    time.sleep(3)
    else:
        for key in keys:
            if config_infomation[key]["type"] == "str":
                while not str_messagebox(key):
                    print("输入值不符合要求，请重新输入")
                    time.sleep(3)
            elif config_infomation[key]["type"] == "bool":
                while not bool_messagebox(key):
                    print("输入值不符合要求，请重新输入")
                    time.sleep(3)
            elif config_infomation[key]["type"] == "list":
                while not list_messagebox(key):
                    print("输入值不符合要求，请重新输入")
                    time.sleep(3)
            elif config_infomation[key]["type"] == "float":
                while not float_messagebox(key):
                    print("输入值不符合要求，请重新输入")
                    time.sleep(3)
            elif config_infomation[key]["type"] == "int":
                while not int_messagebox(key):
                    print("输入值不符合要求，请重新输入")
                    time.sleep(3)

def save_config():
    """
    保存json配置。
    """
    result = yes_no_dialog(
        title="保存配置", text="是否保存配置？"
    ).run()
    if not result:
        return False
    config = {}
    for index in range(len(config_infomation)):
        key = config_infomation[index]["key"]
        value = globals()[key]
        config[key] = value
    with open("configs.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    return True

def load_config():
    """
    加载json配置。
    """
    if not os.path.exists("configs.json"):
        return False
    with open("configs.json", "r", encoding="utf-8") as f:
        config = f.read()
        config = json.loads(config)
    for key in config:
        if key in globals():
            globals()[key] = config[key]
    return True

def select_config():
    """
    选择配置。
    """
    values = []
    for index in range(len(config_infomation)):
        key = config_infomation[index]["key"]
        name = config_infomation[index]["name"]
        values.append((key, name))
    result = checkboxlist_dialog(
        title=f"选择配置",
        values=values
        ).run()
    if result is None:
        return False
    indexs = []
    for key in result:
        for index in range(len(config_infomation)):
            if config_infomation[index]["key"] == key:
                indexs.append(index)
    set_config(indexs)
    return True

if __name__ == "__main__":
    message_dialog(
        title="欢迎使用Muice-Chatbot配置管理",
        text="方向键上下选择配置，空格键确认，Tab键切换选项。"
        ).run()
    if not load_config():
        result = radiolist_dialog(
            values=[("all", '从头设置'), ("select", '选择配置')],
            title="配置管理", text="请选择操作"
            ).run()
        if result == 'select':
            select_config()
        else:
            set_config(keys=[])
    else:
        select_config()
    save_config()