![](src/Cover.png)
<p style="text-align:center">
<img src="https://img.shields.io/github/stars/Moemu/Muice-Chatbot" alt="Stars">
<img src="https://img.shields.io/badge/Model-ChatGLM2--6B & Qwen--7B-green" alt="Model">
<img src="https://img.shields.io/badge/HuggingFace-Dataset-yellow?link=https%3A%2F%2Fhuggingface.co%2Fdatasets%2FMoemu%2FMuice-Dataset" alt="HuggingFace">
<img src="https://img.shields.io/badge/Python-3.10-blue" alt="Python">
</p>

###  3.31更新: 现以提供onebot服务, 您可以使用当前方式来运行，感谢[@MoeSnowyFox](https://github.com/MoeSnowyFox)的贡献！


# 介绍✨

沐雪，一只会**主动**找你聊天的AI女孩子，其对话模型基于[ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B)与[Qwen](https://github.com/QwenLM)微调而成，训练集长度1.8K+ *，具有二次元女孩子的说话风格，比较傲娇，但乐于和你分享生活的琐碎，每天会给你不一样的问候。

*：（训练集长度较低，但我们仍在收集对话数据）

# 功能🪄

✔ 提供本人由1.5k+对话数据微调的ChatGLM2-6B P-Tuning V2模型与Qwen-7B Qlora微调模型（回答原创率：98%+）

✔ 主动发起聊天

✔ 提供5条可用的命令

# 快速开始💻

建议环境：
- Python 3.10
- 一张拥有8GB+ 显存的显卡(int4量化最低要求: 4G ; CPU推理内存要求：16G+)

## 使用 conda

```powershell
git clone https://github.com/Moemu/Muice-Chatbot
cd Muice-Chatbot
conda create --name Muice python=3.10.10
conda activate Muice
pip install -r requirements.txt
```

## 模型下载和加载

目前支持的基底模型如下表：

| 基底模型                                                                                  | 对应微调模型版本号                                | 额外依赖库               |
|---------------------------------------------------------------------------------------|------------------------------------------|---------------------|
| [ChatGLM2-6B-Int4](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b-int4/summary) | 2.2-2.4                                  | cpm_kernels         |
| [ChatGLM2-6B](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b/summary)           | 2.0-2.3                                  |                     |
| [Qwen-7B-Chat-Int4](https://www.modelscope.cn/models/qwen/Qwen-7B-Chat-Int4/summary)  | 2.3                                      | llmtuner            |
| [RWKV(Seikaijyu微调)](https://huggingface.co/Seikaijyu)                                 | 参见[HF](https://huggingface.co/Seikaijyu) | （需要下载配置RWKV-Runner） |

微调模型下载：[Releases](https://github.com/Moemu/Muice-Chatbot/releases)

请将基底模型与微调模型放放入`model`文件夹中（确保微调模型目录下存在.model文件而不是文件夹，部分微调模型由于疏忽还套了一层checkpoint文件夹）

本仓库目前支持如下模型加载方式：

1. 通过API加载
2. 通过transformers的`AutoTokenizer`, `AutoModel`函数加载
3. 通过`llmtuner.chat`(`LLaMA-Factory`)的`ChatModel`类加载
4. 通过`RWKV-Runner`提供的API服务加载

在已测试的模型中，我们建议以下模型通过对应的方式加载，其他模型亦可以通过类似的方式加载：

| 基底模型              | 微调方式        | 加载方法         |
|-------------------|-------------|--------------|
| ChatGLM           | P-tuning V2 | transformers |
| Qwen              | sft         | llmtuner     |
| RWKV(Seikaijyu微调) | pissa       | rwkv-api     |

在配置文件中可调整模型的加载方式：

```json
"model_loader": "api/transformers/llmtuner/rwkv-api",
"model_name_or_path": "基底模型位置",
"adapter_name_or_path": "沐雪微调模型位置"
```

（若是API/rwkv-api加载，`model_name_or_path`填api地址）

## OFA图像识别

若您希望使用OFA图像识别，请在配置文件中设置`enable_ofa_image`为`true`，并设置`ofa_image_model_name_or_path`为OFA图像识别模型的路径。

OFA使用到的依赖需要额外安装：

```powershell
pip install -r ofa_requirements.txt
```

目前建议的基底模型如下表：

| 基底模型                                                                                                                  |
|---------------------------------------------------------------------------------------------------------------------------------|
| [OFA-Image-Caption-Meme-Large-ZH](https://www.modelscope.cn/models/iic/ofa_image-caption_meme_large_zh) |

## 语音回复

若您希望使用语音回复，请在配置文件中设置`Voice_Reply_Rate`为大于0的整数，机器人将会以一定概率回复语音消息。

语音回复使用到的项目：[fishaudio/fish-speech](https://github.com/fishaudio/fish-speech)

在fish-speech的api启动后，更改`fish_speech_api.py`中的`Client`、`reference_audio`、`reference_text`即可。

## 启动实时语音聊天

1.安装依赖：

```powershell
pip install -r audio_requirements.txt
```

2.安装配置语音回复（详见上文）

3.获取语音识别模型

目前建议的基底模型如下表：

| 基底模型                                                                                                                  |
|---------------------------------------------------------------------------------------------------------------------------------|
| [SenseVoice多语言语音理解模型Small](https://www.modelscope.cn/models/iic/SenseVoiceSmall) |

你可以通过以下命令下载并解压模型：

```powershell
modelscope download --model iic/SenseVoiceSmall --local_path ./SenseVoice
```

下载完成后，在配置文件中设置`audio_name_or_path`为模型文件夹的路径。

4.配置信息和设备

你可以通过以下命令查看输入输出设备信息：

```powershell
python test_device_info.py
```
在`realtime_refence.py`中配置输入输出设备信息：

```python

CHUNK = 1024  # 每次读取的音频块大小
FORMAT = pyaudio.paFloat32  # 音频格式
CHANNELS = 1  # 输入设备声道
RATE = 22050  # 采样率（16000/22050/44100）
THRESHOLD = 75  # 声音响度阈值（60-150左右）
SILENCE_THRESHOLD_MS = 1500  # 静音持续时间阈值（毫秒）
SILENCE_COUNT = int(SILENCE_THRESHOLD_MS / (1000 * CHUNK / RATE))  # 静音计数器阈值
use_virtual_device = False  # 是否使用虚拟设备（当你需要通过语音通话时，请设置为True）
if use_virtual_device:
    speaker_device_index = 3  # 输入设备索引
    mic_device_index = 10  # 输出设备索引
    device_index = speaker_device_index
else:
    device_index = 1  # 录音设备索引

```

4.启动实时语音聊天

```powershell
python realtime_refence.py
```

## bot服务配置

现以提供onebot服务支持, 无需担心gocq的风控(喜)

本项目使用[onebotV11](https://github.com/botuniverse/onebot-11)协议, 若您希望于QQ使用, 推荐参考[LLOneBot](https://github.com/LLOneBot/LLOneBot)使用onebot服务

注:请在安装好LLOneBot后, 于设置中开启反向WebSocket服务, 填写`ws://127.0.0.1:21050/ws/api`, 以正常运行

_您也可以使用[Lagrange.Core](https://github.com/LagrangeDev/Lagrange.Core)以及[~~OpenShamrock~~](https://github.com/whitechi73/OpenShamrock)等来链接QQ, 或其他适配器链接其他软件,详见[onebotV11适配器](https://onebot.dev/ecosystem.html#onebot-%E5%AE%9E%E7%8E%B0-1)_

_能使用请勿随意更新ntQQ, 若无法使用请尝试降级ntQQ_

## 总结

在完成这些操作后，你应该得到类似如下所示的文件结构：


```
Muice-Chatbot     <- 主路径
 ├─llm
 ├─model
 │  ├─ chatglm2-6b       <- 原始模型 (三者三选一)
 │  ├─ chatglm2-6b-int4  <- int4原始模型
 │  ├─ Qwen-7B-Chat-Int4 <- Qwen-7B-int4原始模型
 │  └─ Muice
 ├─configs.json  <- 配置文件
 ├─ws.py         <- ws服务
 ├─main.py       <- 主函数
 ├─requirements.txt
 └─...
```


# 配置⚒️

本项目使用`configs.json`作为配置文件，目前支持配置的项如下：

```json
{
    "model_loader": "transformers",
    "model_name_or_path": "./model/chatglm2-6b",
    "adapter_name_or_path": "./model/Muice",
    "enable_ofa_image": false,
    "ofa_image_model_name_or_path": "",
    "Trust_QQ_list": [],
    "AutoCreateTopic": false,
    "read_memory_from_file": true,
    "known_topic_probability": 0.003,
    "time_topic_probability": 0.75,
    "port":21050,
    "bot_qq_id":123456789,
    "Is_CQ_Code": false,
    "Group_Message_Reply_Only_To_Trusted": true,
    "Reply_Rate": 50,
    "At_Reply": false,
    "NonReply_Prefix": [],
    "Voice_Reply_Rate": 0
}
```

`model_loader`: 指定模型加载器的类型，当前支持`api/transformers/llmtuner/rwkv-api`。

`model_name_or_path`: 指定基底模型的名称或路径，例如`./model/chatglm2-6b`。

`adapter_name_or_path`: 指定预训练模型的名称或路径， 例如`./model/Muice`。

`enable_ofa_image`: 是否使用OFA图像识别。

`ofa_image_model_name_or_path`: OFA图像识别模型的名称或路径。

`Trust_QQ_list`: 信任QQ号列表，只有在此列表中的QQ号发送的消息，机器人才会回复。

`AutoCreateTopic`: 是否自动发起新对话。如果启用，将默认以Trust_QQ_list中的第一个QQ号作为对话发起对象。

`read_memory_from_file`: 是否从文件中读取记忆。这对于项目重启后恢复之前的对话状态非常有用。

`known_topic_probability`: 随机发起已知话题的概率。

`time_topic_probability`: 根据时间（早、中、傍、晚）触发日常问候的概率。

`port`: 反向WebSocket服务的端口号，默认`21050`。

`bot_qq_id`: 机器人的QQ号。

`Is_CQ_Code`: 是否启用CQ码处理信息。

`Group_Message_Reply_Only_To_Trusted`: （群聊）是否仅对信任的qq回复。

`Reply_Rate`: （群聊）机器人回复的概率，取值范围为0-100。

`At_Reply`: （群聊）是否只回复@机器人的消息。

`NonReply_Prefix`: 消息前缀，机器人不会回复以这些前缀开头的消息。

`Voice_Reply_Rate`: 语音回复的概率，取值范围为0-100。

# 使用🎉

在本项目根目录下运行 `main.py` 

```powershell
conda activate Muice
python main.py
```

# 命令🕹️

| 命令       | 释义                |
|----------|-------------------|
| /clean   | 清空本轮对话历史          |
| /refresh | 刷新本次对话            |
| /help    | 显示所有可用的命令列表       |
| /reset   | 重置所有对话数据(将存档对话数据) |
| /undo    | 撤销上一次对话           |

# 示例对话（训练集）📑

参见公开的训练集[Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)

# 沐雪人设

与其他聊天机器人项目不同，本项目提供由本人通过自家对话数据集微调后的模型，在Release中提供下载，关于微调后的模型人设，目前公开的信息如下：

![沐雪人设图（若无法打开请通过右键打开）](https://i0.hdslb.com/bfs/new_dyn/9fc79347b54c5f2835884c8f755bd1ea97020216.png)

训练集开源地址： [Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)

原始模型：[THUDM/ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) & [QwenLM/Qwen)](https://github.com/QwenLM/Qwen)

本项目源码使用[MIT license](https://github.com/Moemu/Muice-Chatbot/blob/main/LICENSE)，对于微调后的模型文件，不建议作为商业用途

# 关于🎗️

代码编写：[Moemu](https://github.com/Moemu)

模型训练：[Moemu](https://github.com/Moemu) （RWKV训练：[Seikaijyu](https://github.com/Seikaijyu)）

训练集编写：[Moemu](https://github.com/Moemu)

OneBot服务支持: [MoeSnowyFox](https://github.com/MoeSnowyFox)

代码贡献：

<a href="https://github.com/eryajf/Moemu/Muice-Chatbot/contributors">
  <img src="https://contrib.rocks/image?repo=Moemu/Muice-Chatbot"  alt="图片加载中..."/>
</a>

Star History：

[![Star History Chart](https://api.star-history.com/svg?repos=Moemu/Muice-Chatbot&type=Date)](https://star-history.com/#Moemu/Muice-Chatbot&Date)

