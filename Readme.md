![](src/Cover.png)
<p align="center">
<img src="https://img.shields.io/github/stars/Moemu/Muice-Chatbot" alt="Stars">
<img src="https://img.shields.io/badge/Model-ChatGLM2--6B & Qwen--7B-green" alt="Model">
<img src="https://img.shields.io/badge/HuggingFace-Dataset-yellow?link=https%3A%2F%2Fhuggingface.co%2Fdatasets%2FMoemu%2FMuice-Dataset" alt="HuggingFace">
<img src="https://img.shields.io/badge/Python-3.10-blue" alt="Python">
</p>
本文档同时提供[繁體中文版（不建议）](https://github.com/Moemu/Muice-Chatbot/blob/main/Readme_zh-tw.md)

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
- 一张拥有13GB+ 显存的显卡(int4量化最低要求: 4G/CPU推理内存要求：16G+)

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

## go-cqhttp配置

本项目使用[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)进行机器人交互，请从[Releases](https://github.com/Mrs4s/go-cqhttp/releases)下载相应平台的可执行程序，并放入 `qqbot` 目录中

有关go-cqhttp 的详细配置方法及问题，请访问 [go-cqhttp 主页](https://docs.go-cqhttp.org/) 及其 [Github 页面](https://github.com/Mrs4s/ go-cqhttp)

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
 ├─qqbot
 │  ├─go-cqhttp.exe
 │  └─...
 ├─configs.json  <- 配置文件
 ├─main.py       <- 主函数
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

在本项目根目录下运行 `main.py` 

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

# 示例对话（训练集）

参见公开的训练集[Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)

# 沐雪人设

与其他聊天机器人项目不同，本项目提供由本人通过自家对话数据集微调后的模型，在Release中提供下载，关于微调后的模型人设，目前公开的信息如下：

![沐雪人设图（若无法打开请通过右键打开）](https://i0.hdslb.com/bfs/new_dyn/9fc79347b54c5f2835884c8f755bd1ea97020216.png)

训练集开源地址： [Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)

原始模型：[THUDM/ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B)

本项目源码使用[MIT license](https://github.com/Moemu/Muice-Chatbot/blob/main/LICENSE)，对于微调后的模型文件，不建议作为商业用途

# 关于🎗️

代码编写：[Moemu](https://github.com/Moemu)

安装及配置指南编写：[TurboHK](https://github.com/TurboHK)

模型训练：[Moemu](https://github.com/Moemu)

训练集编写：[Moemu](https://github.com/Moemu)

代码贡献：

<a href="https://github.com/eryajf/Moemu/Muice-Chatbot/contributors">
  <img src="https://contrib.rocks/image?repo=Moemu/Muice-Chatbot" />
</a>

Star History：

[![Star History Chart](https://api.star-history.com/svg?repos=Moemu/Muice-Chatbot&type=Date)](https://star-history.com/#Moemu/Muice-Chatbot&Date)

