![](src/Cover.png)
<p align="center">
<img src="https://img.shields.io/github/stars/Moemu/Muice-Chatbot" alt="Stars">
<img src="https://img.shields.io/badge/Model-ChatGLM2--6B & Qwen--7B-green" alt="Model">
<img src="https://img.shields.io/badge/HuggingFace-Dataset-yellow?link=https%3A%2F%2Fhuggingface.co%2Fdatasets%2FMoemu%2FMuice-Dataset" alt="HuggingFace">
<img src="https://img.shields.io/badge/Python-3.10-blue" alt="Python">
</p>


### 10.20更新：我们已无力提供对qqbot相关代码的更新，详见https://github.com/Moemu/Muice-Chatbot/issues/18 ，目前我们打算提供一个前端页面来完成对沐雪的任何交互，对此带来的不便我深感歉意。

##   3.31现以提供onebot服务, 您可以使用当前方式来运行

### 由于本作者现在正在高三备战高考，因此可能无法及时处理任何问题/频繁提供更新，感谢您的谅解

本文档同时提供[繁體中文版](https://github.com/Moemu/Muice-Chatbot/blob/main/Readme_zh-tw.md)

# 介绍✨

沐雪，一只会**主动**找你聊天的AI女孩子，其对话模型基于[ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B)微调而成，训练集长度1.3K+ *，具有二次元女孩子的说话风格，比较傲娇，但乐于和你分享生活的琐碎，每天会给你不一样的问候。

*：（训练集长度较低，但我们仍在收集对话数据）

# 功能🪄

✔ 提供本人由1.5k+对话数据微调的ChatGLM2-6B P-Tuning V2模型与Qwen-7B Qlora微调模型（回答原创率：98%+）

✔ 主动发起聊天（局限于已有的Prompt）

✔ 提供5条可用的命令

# 安装💻

建议环境：
- Python 3.10
- 一张拥有13GB+ 显存的显卡(int4量化最低要求: 5.5G/CPU推理内存要求：16G+)

## 使用 conda

```powershell
git clone https://github.com/Moemu/Muice-Chatbot
cd Muice-Chatbot
conda create --name Muice python=3.10.10
conda activate Muice
pip install -r requirements.txt
```

## 克隆原始模型

下面三个选一个就好了

```powershell
mkdir model
cd model
git lfs install
git clone https://huggingface.co/THUDM/chatglm2-6b
cd ..
```

## 克隆原始模型（int4量化）

```powershell
mkdir model
cd model
git lfs install
git clone https://huggingface.co/THUDM/chatglm2-6b-int4
cd ..
pip install cpm_kernels
```

## 克隆Qwen-7B原始模型（int4量化）

```powershell
mkdir model
cd model
git lfs install
git clone https://huggingface.co/Qwen/Qwen-7B-Chat-Int4
cd ..
pip install peft
pip install optimum
pip install auto-gptq
```

## 克隆沐雪微调模型

在[Releases](https://github.com/Moemu/Muice-Chatbot/releases)上下载微调后的模型压缩包，解压后命名为`Muice`并放置于`model`文件夹中以使用我们的微调模型

## bot服务配置

~本项目使用[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)进行机器人交互，请从[Releases](https://github.com/Mrs4s/go-cqhttp/releases)下载相应平台的可执行程序，并放入 `qqbot` 目录中~

~有关go-cqhttp 的详细配置方法及问题，请访问 [go-cqhttp 主页](https://docs.go-cqhttp.org/) 及其 [Github 页面](https://github.com/Mrs4s/ go-cqhttp)~

现以提供onebot服务支持, 无需担心gocq的风控

本项目使用[onebotV11](https://github.com/botuniverse/onebot-11)协议, 若您希望于QQ使用, 推荐参考[LLOneBot](https://github.com/LLOneBot/LLOneBot)使用onebot服务

注:请在安装好LLOneBot后, 于设置中开启HTTP服务, 监听端口填写`8010`, 开启HTTP事件上报, 上报地址填写`http://127.0.0.1:8020` 以正常运行

## 总结

在完成这些操作后，你应该得到类似如下所示的文件结构：
```
Muice-Chatbot    <- 主路径
 ├─llm
 ├─model
 │  ├─ chatglm2-6b <- 原始模型 (三者三选一)
 │  ├─ chatglm2-6b-int4 <- int4原始模型
 │  ├─ Qwen-7B-Chat-Int4 <- Qwen-7B-int4原始模型
 │  └─ Muice
 ├─configs.json  <- 配置文件
 ├─main.py       <- 主函数
 ├─onebot.py     <- onebot服务
 ├─defqq.py      <- onebot函数
 ├─requirements.txt
 └─...
```

# 配置⚒️

本项目使用`configs.json`作为配置文件，目前支持配置的项如下：

```json
{
    "Trust_QQ_list": [],
    "AutoCreateTopic": false,
    "read_memory_from_file": true,
    "known_topic_probability": "0.003",
    "time_topic_probability": "0.75"
}
```

`Trust_QQ_list`: 信任QQ号列表，只有在列表的QQ号，沐雪才会回复（留空为全部处理）

`AutoCreateTopic`: 是否自动发起新对话，默认以Trust_QQ_list的第0项作为发起新对话对象

`read_memory_from_file`: 从文件中读取记忆，用于项目重启后加载原来的记忆

`known_topic_probability`: 概率：随机发起一个已知的话题

`time_topic_probability`: 概率：早、中、傍、晚触发日常问候

# 使用🎉

在本项目根目录下运行 `onebot.py` 

```powershell
conda activate Muice
python onebot.py
```

# 命令🕹️

|  命令   | 释义  |
|  ----  | ----  |
| /clean  | 清空本轮对话历史 |
| /refresh  | 刷新本次对话 |
| /help  | 显示所有可用的命令列表 |
| /reset  | 重置所有对话数据(将存档对话数据) |
| /undo  | 撤销上一次对话 |

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

# 提报 Issue

> 请注意, 开发者并没有义务回复您的问题. 您应该具备基本的提问技巧。  
> 有关如何提问，请阅读[《提问的智慧》](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md)

训练集开源地址： [Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)

原始模型：[THUDM/ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B)

本项目源码使用[MIT license](https://github.com/Moemu/Muice-Chatbot/blob/main/LICENSE)，对于微调后的模型文件，不建议作为商业用途

# 关于🎗️

代码编写：[Moemu](https://github.com/Moemu)

安装及配置指南编写：[TurboHK](https://github.com/TurboHK)

模型训练：[Moemu](https://github.com/Moemu)

训练集编写：[Moemu](https://github.com/Moemu)

OneBot支持:[MoeSnowyFox](https://github.com/MoeSnowyFox)

代码贡献：

<a href="https://github.com/eryajf/Moemu/Muice-Chatbot/contributors">
  <img src="https://contrib.rocks/image?repo=Moemu/Muice-Chatbot" />
</a>

Star History：

[![Star History Chart](https://api.star-history.com/svg?repos=Moemu/Muice-Chatbot&type=Date)](https://star-history.com/#Moemu/Muice-Chatbot&Date)

