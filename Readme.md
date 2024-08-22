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
    "Trust_QQ_list": [],
    "AutoCreateTopic": false,
    "read_memory_from_file": true,
    "known_topic_probability": 0.003,
    "time_topic_probability": 0.75,
    "port":21050,
    "bot_qq_id":123456789,
    "Is_OneBot_Plugin": false,
}
```

`model_loader`: 指定模型加载器的类型，当前支持`api/transformers/llmtuner/rwkv-api`。

`model_name_or_path`: 指定基底模型的名称或路径，例如`./model/chatglm2-6b`。

`adapter_name_or_path`: 指定预训练模型的名称或路径， 例如`./model/Muice`。

`Trust_QQ_list`: 信任QQ号列表，只有在此列表中的QQ号发送的消息，机器人才会回复。

`AutoCreateTopic`: 是否自动发起新对话。如果启用，将默认以Trust_QQ_list中的第一个QQ号作为对话发起对象。

`read_memory_from_file`: 是否从文件中读取记忆。这对于项目重启后恢复之前的对话状态非常有用。

`known_topic_probability`: 随机发起已知话题的概率。

`time_topic_probability`: 根据时间（早、中、傍、晚）触发日常问候的概率。

`port`: 反向WebSocket服务的端口号，默认`21050`。

`bot_qq_id`: 机器人的QQ号。

`Is_OneBot_Plugin`: 当抛出错误`data['message'] 不是列表`时将此选项设置为true。

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

