![](src/Cover.png)
<p align="center">
<img src="https://img.shields.io/github/stars/Moemu/Muice-Chatbot" alt="Stars">
<img src="https://img.shields.io/badge/Model-ChatGLM2--6B-green" alt="Model">
<img src="https://img.shields.io/badge/Python-3.10-blue" alt="Python">
</p>


# 介绍✨

沐雪，一只会**主动**找你聊天的AI女孩子，其对话模型基于[ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B)微调而成，训练集长度1.3K+ *，具有二次元女孩子的说话风格，比较傲娇，但乐于和你分享生活的琐碎，每天会给你不一样的问候。

*：（训练集长度较低，但我们仍在收集对话数据）

# 功能🪄

✔ 提供本人由1.3k+对话数据微调的ChatGLM2-6B P-Tuning V2模型（回答原创率：98%+）

✔ 主动发起聊天（局限于已有的Prompt）

✔ 提供5条可用的命令

# 安装💻

建议环境：Python 3.10  GPU显存16G以上

## 使用 conda

```powershell
git clone https://github.com/Moemu/Muice-Chatbot
cd Muice-Chatbot
conda create --name Muice python=3.10.10
conda activate Muice
pip install -r requirements.txt
```

## 克隆模型

```
mkdir model
cd model
git clone https://huggingface.co/THUDM/chatglm2-6b
cd ..
```

除此之外，在[Releases](https://github.com/Moemu/Muice-Chatbot/releases)上下载微调后的模型压缩包，解压后命名为`Muice`并放置于`model`文件夹中以使用我们的微调模型

## go-cqhttp配置

本项目使用[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)进行机器人交互，请从[Releases](https://github.com/Mrs4s/go-cqhttp/releases)下载相应平台的可执行程序，并放入 `bot` 目录中

# 配置⚒️

本项目使用`configs.json`作为配置文件，目前支持配置的项如下：

```json
{
    // 信任QQ号列表，只有在列表的QQ号，沐雪才会回复
    "Trust_QQ_list": [
        123456789,
        987654321
    ],
    // 是否自动发起新对话，默认以Trust_QQ_list的第0项作为发起新对话对象
    "AutoCreateTopic": false,
    // 从文件中读取记忆，用于项目重启后加载原来的记忆
    "read_memory_from_file": true,
    // 概率：随机发起一个已知的话题
    "known_topic_probability": "0.003",
    // 概率：早、中、傍、晚触发日常问候
    "time_topic_probability": "0.75"
}
```

# 使用🎉
运行 `main.py` 即可

```powershell
conda activate Muice
python main.py
```

# 命令🕹️

## /clean

清空本轮对话历史

## /refresh

刷新本次对话

## /help

显示所有可用的命令列表

## /reset

重置所有对话数据(将存档对话数据)

## /undo

撤销上一次对话

# 示例对话

Q: 你好

> 你好，你今天感觉怎么样？

Q: 你知道猫娘嘛

> 唔...不太知道喵...

Q: 雪雪喜欢吃什么？

>吃·你·而已

Q: 工作又忙又累，还要加班什么的（此回答不稳定）

> 赚钱嘛，总是伴随着一些苦逼的活

# 沐雪人设

与其他聊天机器人项目不同，本项目提供由本人通过自家对话数据集微调后的模型，在Release中提供下载，关于微调后的模型人设，目前公开的信息如下：

> 姓名：沐雪
> 性别：女？
> 年龄：16岁？
> 生日：06.12
> 性格：微傲，喜欢用"本雪"来称呼自己，但很会关心别人。害怕独自一个人，不和她聊天的时候她会**主动**找你聊天

# 已知问题

1. 对于以下问题，模型回答的泛化性较差

   （创造一个新话题）、雪雪最近有没有什么值得分享的事情？

   对应策略：未来将会对训练集进行调整，在此之前建议将配置项中的`known_topic_probability`调至0

# 关于🎗️

代码编写：Moemu

模型训练：Moemu

训练集编写：Moemu

原始模型：[THUDM/ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B)

本项目源码使用[MIT license](https://github.com/Moemu/Muice-Chatbot/blob/main/LICENSE)，对于微调后的模型文件，不建议作为商业用途

