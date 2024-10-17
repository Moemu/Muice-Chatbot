![](src/Cover.png)
<p style="text-align:center">
<img src="https://img.shields.io/github/stars/Moemu/Muice-Chatbot" alt="Stars">
<img src="https://img.shields.io/badge/Model-ChatGLM2--6B & Qwen--7B-green" alt="Model">
<img src="https://img.shields.io/badge/HuggingFace-Dataset-yellow?link=https%3A%2F%2Fhuggingface.co%2Fdatasets%2FMoemu%2FMuice-Dataset" alt="HuggingFace">
<img src="https://img.shields.io/badge/Python-3.10-blue" alt="Python">
</p>


# 介绍✨

沐雪，一只会**主动**找你聊天的 AI 女孩子，其对话模型基于 [ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) 与 [Qwen](https://github.com/QwenLM) 微调而成，训练集体量 3k+ ，具有二次元女孩子的说话风格，比较傲娇，但乐于和你分享生活的琐碎，每天会给你不一样的问候。

# 功能🪄

✅ 支持近乎全自动安装环境

✅ 提供本人由 3k+ 对话数据微调的 ChatGLM2-6B P-Tuning V2 模型与 Qwen Qlora 微调模型	

✅ 主动发起聊天（随机和每天早中晚固定时间）

✅ 提供 5 条命令以便在聊天中进行刷新回复等操作

✅ OFA 图像识别：识别表情包、理解表情包、发送表情包

✅ 支持通过 [fishaudio/fish-speech](https://github.com/fishaudio/fish-speech) 进行语言合成（沐雪 TTS 模型尚未发布）

✅ 在群聊中聊天（支持被 @ 回复或不被 @ 随机回复）

✅ 在控制台中实时对话（暂不支持打 QQ 语音）

⬜ （TODO）对记忆模块进行优化，实现长期记忆与短期记忆

# 快速开始💻

建议环境：

- Python 3.10+
- 一张拥有 6GB 及以上显存的显卡（int4 量化最低要求为 4G 显存，CPU 推理需要 16G 及以上内存）

## 自动安装

目前已做到自动安装所有软件、依赖，通过 `Code -> Download ZIP` 下载解压最新源码。

双击 `install_env.bat` 安装（**不能启用旧版控制台**），或在命令行中运行以下命令：

```powershell
.\install_env.bat
```

自动安装可能需要较长时间，请耐心等待，安装完成后，你仍需手动下载模型。

**自动安装脚本使用的是 Python 虚拟环境，不需要 Conda，请留意安装脚本的提示。**

## 手动安装（使用 Conda）

```powershell
git clone https://github.com/Moemu/Muice-Chatbot
cd Muice-Chatbot
conda create --name Muice python=3.10.10
conda activate Muice
pip install -r requirements.txt
```

## 模型下载和加载

目前支持的基底模型如下表：

| 基底模型                                                     | 对应微调模型版本号                         | 额外依赖库                  |
| ------------------------------------------------------------ | ------------------------------------------ | --------------------------- |
| [ChatGLM2-6B-Int4](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b-int4/summary) | 2.2-2.4                                    | cpm_kernels                 |
| [ChatGLM2-6B](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b/summary) | 2.0-2.3                                    |                             |
| [Qwen-7B-Chat-Int4](https://www.modelscope.cn/models/qwen/Qwen-7B-Chat-Int4/summary) | 2.3、2.6.2                                 | llmtuner                    |
| [Qwen2-1.5B-Instruct-GPTQ-Int4](https://www.modelscope.cn/models/qwen/Qwen2-1.5B-Instruct-GPTQ-Int4/summary) | 2.5.3                                      | llmtuner                    |
| [RWKV(Seikaijyu微调)](https://huggingface.co/Seikaijyu)      | 参见 [HF](https://huggingface.co/Seikaijyu) | （需要下载配置 RWKV-Runner） |

微调模型下载：[Releases](https://github.com/Moemu/Muice-Chatbot/releases)

请将基底模型与微调模型放入 `model` 文件夹中（确保微调模型目录下存在 `.model` 文件而不是文件夹，部分微调模型由于疏忽还套了一层 `checkpoint` 文件夹）

本仓库目前支持如下模型加载方式：

1. 通过 API 加载
2. 通过 `transformers` 的`AutoTokenizer`, `AutoModel` 函数加载
3. 通过`llmtuner.chat`（`LLaMA-Factory`）的 `ChatModel` 类加载
4. 通过 `RWKV-Runner` 提供的 API 服务加载

在已测试的模型中，我们建议以下模型通过对应的方式加载，其他模型亦可以通过类似的方式加载：

| 基底模型              | 微调方式        | 加载方法         |
|-------------------|-------------|--------------|
| ChatGLM           | P-tuning V2 | transformers |
| Qwen              | sft         | llmtuner     |
| RWKV（Seikaijyu 微调） | pissa       | rwkv-api     |

在配置文件中可调整模型的加载方式：

```json
"model_loader": "api/transformers/llmtuner/rwkv-api",
"model_name_or_path": "<基底模型位置>",
"adapter_name_or_path": "<沐雪微调模型位置>"
```

（若是 API / rwkv-api 加载，`model_name_or_path` 填写对应的 API 地址）

如果你没有合适的显卡，需要通过 CPU 加载模型，请安装并配置 `GCC` 环境，然后勾选 `openmp`.

## Faiss 长期记忆（实验性内容）

本项目支持 Faiss 向量记忆，即将聊天记录保存至 Faiss 中，以便长期记忆。

若您希望使用 Faiss 向量记忆，请在配置文件中设置 `enable_faiss` 为 `true`，并设置 `sentence_transformer_model_name_or_path` 为 `sentence-transformers` 模型的路径。

Faiss 记忆用到的 `sentence-transformers` 模型需要额外下载（理论上所有 `sentence-transformers` 模型都可以）：

| 推荐 `sentence-transformers` 模型                                                      |
| ------------------------------------------------------------ |
| [distiluse-base-multilingual-cased-v1](https://hf-mirror.com/sentence-transformers/distiluse-base-multilingual-cased-v1)|

Faiss 向量库位于 `memory` 文件夹中，一共三个文件：`faiss_index.faiss`、`faiss_index.faiss.docstore`、`faiss_index.faiss.mapping`，三者一一对应，改动前请注意备份。

### 导入 CSV 记忆

下载 CSV 记忆文件，确保其内部格式（**UTF-8**）为：

```csv
topic1\tcontent1
topic2\tontent2
...
```

将文件放入根目录，运行导入程序：

```powershell
python import_csv_memory.py
```

输入文件名（**包括 `.csv` 后缀**），程序将自动导入 Faiss 向量库中。

## OFA 图像识别（识别 / 发送表情包）

本项目支持 OFA 图像识别，即对聊天图片进行特征提取，并通过 OFA 模型进行描述生成。发送信息时，会检索本地图片库，若存在匹配的图片，则会发送图片。

若您希望使用OFA图像识别，请在配置文件中设置 `enable_ofa_image` 为 `true`，并设置 `ofa_image_model_name_or_path` 为 OFA 图像识别模型的路径。

OFA 使用到的依赖需要额外安装：

```powershell
conda activate Muice
pip install -r ofa_requirements.txt
```

目前支持的 OFA 模型如下表：

| OFA 模型                                                      |
| ------------------------------------------------------------ |
| [OFA-Image-Caption-Meme-Large-ZH](https://www.modelscope.cn/models/iic/ofa_image-caption_meme_large_zh) （建议） |
| [ofa_image-caption_muge_base_zh](https://www.modelscope.cn/models/iic/ofa_image-caption_muge_base_zh) |

本地图片数据库位于 `image_data` 文件夹中，程序会每五分钟备份一次数据库，默认保留5个备份槽位。

若您想要回退数据库到某个时间点，请将 `image_data` 文件夹中的 `image_data.db` 删除，并将备份槽位文件 `image_data.db.backup_xxx_xxx` 修改为 `image_data.db`。

## 语音回复

若您希望使用语音回复，请在配置文件中设置 `Voice_Reply_Rate` 为大于 0 的整数，机器人将会以设置的概率回复语音消息。

语音回复使用到的项目：[fishaudio/fish-speech](https://github.com/fishaudio/fish-speech)

在 fish-speech 的 WebUI 启动（使用 `--infer` 参数）后，更改 `fish_speech_api.py` 中的 `Client`、`reference_audio`、`reference_text` 即可。

- `Client` 为 fish-speech 的 WebUI 地址

- `reference_audio` 为参考音频文件路径，此音频用于变声效果。

- `reference_text` 为参考音频文件的参考文本。

## 启动实时语音聊天

1.安装依赖：

```powershell
conda activate Muice
pip install -r audio_requirements.txt
```

2.安装配置语音回复（详见上文）

3.获取语音识别模型

目前支持的模型如下表：

| 语音识别模型                                                                                                                  |
|---------------------------------------------------------------------------------------------------------------------------------|
| [SenseVoice 多语言语音理解模型 Small](https://www.modelscope.cn/models/iic/SenseVoiceSmall) |

你可以通过以下命令下载并解压模型：

```powershell
modelscope download --model iic/SenseVoiceSmall --local_path ./SenseVoice
```

下载完成后，在配置文件中设置 `audio_name_or_path` 为模型文件夹的路径。

4.配置信息和设备

你可以通过以下命令查看输入输出设备信息：

```powershell
python realtime_refence.py --get_device
```
在 `realtime_refence.py` 中配置输入输出设备信息：

```python

CHUNK = 1024  # 每次读取的音频块大小
FORMAT = pyaudio.paFloat32  # 音频格式
CHANNELS = 1  # 输入设备声道
RATE = 22050  # 采样率（16000/22050/44100）
THRESHOLD = 75  # 声音响度阈值（60-150左右，请根据实际情况调节）
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

## Bot 服务配置

现以提供 OneBot 服务支持, 无需担心 gocq 的风控(喜)

本项目使用 [OneBot V11](https://github.com/botuniverse/onebot-11) 协议, 若您希望于 QQ 使用, 推荐参考 [LLOneBot](https://github.com/LLOneBot/LLOneBot) 使用 OneBot 服务

注：请在安装好 LLOneBot 后, 于设置中开启反向 WebSocket 服务, 填写 `ws://127.0.0.1:21050/ws/api`, 以正常运行

您也可以使用 [Lagrange.Core](https://github.com/LagrangeDev/Lagrange.Core) 以及 [~~OpenShamrock~~](https://github.com/whitechi73/OpenShamrock) 等来链接QQ, 或其他适配器链接其他软件，详见 [OneBot V11 适配器](https://onebot.dev/ecosystem.html#onebot-%E5%AE%9E%E7%8E%B0-1)

**能使用请勿随意更新 QQNT, 若无法使用请尝试降级 QQNT**

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

本项目配置文件为 `configs.json`，目前支持配置的项如下：

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
    "Reply_Wait": true,
    "bot_qq_id":123456789,
    "Is_CQ_Code": false,
    "Group_Message_Reply_Only_To_Trusted": true,
    "Reply_Rate": 50,
    "At_Reply": false,
    "NonReply_Prefix": [],
    "Voice_Reply_Rate": 0
}
```

`model_loader`: 指定模型加载器的类型，当前支持 `api/transformers/llmtuner/rwkv-api`。

`model_name_or_path`: 指定基底模型的名称或路径，例如 `./model/chatglm2-6b`。

`adapter_name_or_path`: 指定预训练模型的名称或路径， 例如 `./model/Muice`。

`enable_ofa_image`: 是否使用 OFA 图像识别。

`ofa_image_model_name_or_path`: OFA 图像识别模型的名称或路径。

`Trust_QQ_list`: 信任 QQ 号列表，只有在此列表中的 QQ 号发送的消息，机器人才会回复。

`AutoCreateTopic`: 是否自动发起新对话。如果启用，将默认以 Trust_QQ_list 中的第一个 QQ 号作为对话发起对象。

`read_memory_from_file`: 是否从文件中读取记忆。这对于项目重启后恢复之前的对话状态非常有用。

`known_topic_probability`: 随机发起已知话题的概率。

`time_topic_probability`: 根据时间（早、中、傍、晚）触发日常问候的概率。

`port`: 反向WebSocket服务的端口号，默认 `21050`。

`Reply_Wait`: （私聊）是否回复时等待一段时间。

`bot_qq_id`: 机器人的 QQ 号。

`Is_CQ_Code`: 是否启用 CQ 码处理信息。

`Group_Message_Reply_Only_To_Trusted`: （群聊）是否仅对信任的 QQ 回复。

`Reply_Rate`: （群聊）机器人回复的概率，取值范围为 0-100。

`At_Reply`: （群聊）是否只回复 @ 机器人的消息。

`NonReply_Prefix`: 消息前缀，机器人不会回复以这些前缀开头的消息。

`Voice_Reply_Rate`: 语音回复的概率，取值范围为 0-100。

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

参见公开的训练集 [Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)

# 沐雪人设

与其他聊天机器人项目不同，本项目提供由本人通过自家对话数据集微调后的模型，在 Release 中提供下载，关于微调后的模型人设，目前公开的信息如下：

![沐雪人设图（若无法打开请通过右键打开）](https://i0.hdslb.com/bfs/new_dyn/9fc79347b54c5f2835884c8f755bd1ea97020216.png)

训练集开源地址： [Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)

原始模型：[THUDM/ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) & [QwenLM/Qwen](https://github.com/QwenLM/Qwen)）

本项目源码使用 [MIT License](https://github.com/Moemu/Muice-Chatbot/blob/main/LICENSE)，对于微调后的模型文件，不建议将其作为商业用途

# 关于🎗️

代码实现：[Moemu](https://github.com/Moemu)、[MoeSnowyFox](https://github.com/MoeSnowyFox)、[NaivG](https://github.com/NaivG)

训练集编写与模型微调：[Moemu](https://github.com/Moemu) （RWKV 微调：[Seikaijyu](https://github.com/Seikaijyu)）

总代码贡献：

<a href="https://github.com/eryajf/Moemu/Muice-Chatbot/contributors">
  <img src="https://contrib.rocks/image?repo=Moemu/Muice-Chatbot"  alt="图片加载中..."/>
</a>

Star History：

[![Star History Chart](https://api.star-history.com/svg?repos=Moemu/Muice-Chatbot&type=Date)](https://star-history.com/#Moemu/Muice-Chatbot&Date)

