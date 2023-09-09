![](src/Cover.png)
<p align="center">
<img src="https://img.shields.io/github/stars/Moemu/Muice-Chatbot" alt="Stars">
<img src="https://img.shields.io/badge/Model-ChatGLM2--6B-green" alt="Model">
<img src="https://img.shields.io/badge/Python-3.10-blue" alt="Python">
</p>

<p align="center">
  <a href="https://github.com/Moemu/Muice-Chatbot/blob/main/Readme_zh-tw.md">繁体中文版</a>
</p>

# 介绍✨

沐雪，一只会**主动**找你聊天的AI女孩子，其对话模型基于[ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) 微调而成，训练集长度1.3K+ *，具有二次元女孩子的说话风格，比较傲娇，但乐于和你分享生活的琐碎，每天会给你不一样的问候。

*：（训练集长度较低，但我们仍在收集对话数据）

# 功能🪄

✔ 提供本人由 1.3k+ 对话数据微调的 ChatGLM2-6B P-Tuning V2 模型（回答原创率：98%+）

✔ 主动发起聊天（局限于已有的 Prompt）

✔ 提供5条可用的命令

# 使用前须知⚠️
- **本项目不适合零基础的小白使用!**
- 该项目依赖pytorch，若不使用支援[ CUDA （Compute Unified Device Architecture，统一计算架构） ](https://developer.nvidia.com/about-cuda) 的显卡（NVIDIA 系列显示卡），处理效率会大幅降低。



# Windows 版本安装及配置指南🪟

## 1. 最佳系统配置
- 作业系统：Windows 10 及以上/Windows Server 2012 及以上
- 处理器：x86 架构（ARM 可能会出现意料之外的问题）
- 显示卡：支援 CUDA 运算，16GB 及以上显示记忆体（在日后的更新中，将会针对显示记忆体需求高的问题进行优化）

## 2. 配置运行环境

###  安装 Python 3.10.9

#### 1. 从 [Python.org](https://www.python.org/downloads/release/python-3109/) 下载适合您系统的安装包
#### 2. 安装选项选择 ```Install for All Users``` 及 ```Add to PATH```
#### 3. 完成安装

### 安装 conda
#### 1. 从 [Anacoda.com](https://www.anaconda.com/download/) 下载适合您系统的安装包
#### 2. 安装选项选择 ```Install for All Users``` 及 ```Add to PATH```

### 添加 conda 至系统环境变量中
#### 1. 右键点按```此电脑```（```This PC```）−−>```属性```（```Porperties```）
#### 2. 找到```高级系统设置```（```Advanced System Settings```）−−>```环境变量```（```Environment Variables...``）
#### 3. 在```用户变量```（```User variables for [Your Username]``` ）中找到```Path```一栏，点选```编辑`` `（```Edit```）−−>```新增```（```New```），新增 Anacoda 路径。 （预设路径为```C:\ProgramData\anaconda3\Library\bin```、```C:\ProgramData\anaconda3\Scripts```和```C:\ProgramData\anaconda3```，这三者都需要新增到Path 中）

### 安装 Pytorch
#### 1. 从[Pytorch.org](https://pytorch.org/get-started/locally/) 产生并复制适合您设备统的命令（请在```Package``` 一栏中选择```conda```，在```Language``` 一栏中选择```Python```；若您的显示卡支持 CUDA，请在```Compute Platform``` 一栏选择相应的 CUDA 版本，否则选```CPU```）
#### 2. 在您的设备上使用管理员权限启动 ```命令提示符```（```cmd```），粘贴并执行上一步复制的安装命令，等待安装完成


## 3. 安装及配置项目

### 使用 conda

#### 在 Powershell 中执行下列命令：

```Powershell
git clone https://github.com/Moemu/Muice-Chatbot
cd Muice-Chatbot
conda create --name Muice python=3.10.9
conda activate Muice
pip install -r requirements.txt
```

### 克隆模型

#### 在上一步产生的 `Muice-Chatbot` 资料夹中执行下列命令：
```
mkdir model
cd model
git lfs install
git clone https://huggingface.co/THUDM/chatglm2-6b
cd ..
```
档案较大，下载需时较久，请耐心等待。

### 下载微调后的模型压缩文件

从 [Releases](https://github.com/Moemu/Muice-Chatbot/releases) 下载微调后的模型压缩档，解压缩后将其重新命名为 `Muice` 并置于 `model` 文件夹中


### 配置 go-cqhttp
本项目目使用[go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 进行机器人交互，请从其[Releases](https://github.com/Mrs4s/go-cqhttp/releases ) 中下载相应的版本及处理程式，并置于`qqbot` 文件夹中

有关go-cqhttp 的详细配置方法及问题，请访问 [go-cqhttp 主页](https://docs.go-cqhttp.org/) 及其 [Github 页面](https://github.com/Mrs4s/ go-cqhttp)

### 档案结构
在最后，您应该得到类似如下所示的文件结构：
```
Muice-Chatbot    <- 主路径
 ├─llm
 ├─model
 │  ├─ chatglm2-6b
 │  └─ Muice
 ├─qqbot
 │  ├─go-cqhttp.exe
 │  └─...
 ├─configs.json  <- Muice 设定档
 ├─main.py       <- 主处理程序
 ├─requirements.txt
 └─...
```

### 配置 Muice
本项目使用 `configs.json` 作为设定档，目前支援如下功能：

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

## 4. 启动
在根路径（```Muice-Chatbot``` 资料夹）中开启 Powershell，逐行键入以下命令：
```powershell
conda activate Muice
python main.py
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

与其他聊天机器人项目不同，本项目提供由本人通过自家对话数据集微调后的模型，在 Release 中提供下载，关于微调后的模型人设，目前公开的信息如下：

> 姓名：沐雪

> 性别：女？

> 年龄：16岁？

> 生日：06.12

> 性格：微傲，喜欢用"本雪"来称呼自己，但很会关心别人。害怕独自一个人，不和她聊天的时候她会**主动**找你聊天

# 已知问题

1. 对于以下问题，模型回答的泛化性较差

   （创造一个新话题）、雪雪最近有没有什么值得分享的事情？

   对应策略：未来将会对训练集进行调整，在此之前建议将配置项中的`known_topic_probability`调至0
   

# 提报 Issue
> 请注意, 开发者并没有义务回复您的问题. 您应该具备基本的提问技巧。
> 有关如何提问，请阅读[《提问的智慧》](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way#readme)


# 关于🎗️

代码编写：[Moemu](https://github.com/Moemu)

安装及配置指南编写：[TurboHK](https://github.com/TurboHK)

模型训练：[Moemu](https://github.com/Moemu)

训练集编写：[Moemu](https://github.com/Moemu)


原始模型：[THUDM/ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B)

本项目源码使用 [MIT license](https://github.com/Moemu/Muice-Chatbot/blob/main/LICENSE)，对于微调后的模型文件，不建议作为商业用途
