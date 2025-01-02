![](src/Cover.png)
<p style="text-align:center">
<img src="https://img.shields.io/github/stars/Moemu/Muice-Chatbot" alt="Stars">
<img src="https://img.shields.io/badge/Model-ChatGLM2--6B & Qwen--7B-green" alt="Model">
<img src="https://img.shields.io/badge/HuggingFace-Dataset-yellow?link=https%3A%2F%2Fhuggingface.co%2Fdatasets%2FMoemu%2FMuice-Dataset" alt="HuggingFace">
<img src="https://img.shields.io/badge/Python-3.10-blue" alt="Python">
</p>

简体中文 | [繁體中文](./docs/Readme_tc.md) | [English](./docs/Readme_en.md) | [日本語](./docs/Readme_jp.md) 

> [!IMPORTANT]
> 
> 2025.01.02 更新：本项目依赖于 LiteLoaderQQNT 框架。自 2024.11.23 起，陆续有用户反馈自己使用该框架而被封号的事件（[#1032](https://github.com/LiteLoaderQQNT/LiteLoaderQQNT/issues/1032)）。需要声明的一点是，本 Repo 与此次封号事件无直接关联，但继续使用此 Repo 有着被封号的风险，继续使用则代表您承认此后所遭遇到的账号问题与本 Repo 无关
> 
> 2024.12.04 更新：由于配置文件格式变更，如果先前你拉取过本 Repo 并在12.04后执行过 fetch 操作，请您重新设置配置文件，由此带来的不便我们深表歉意


# 介绍✨

沐雪，一只会**主动**找你聊天的 AI 女孩子，其对话模型基于 [ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) 与 [Qwen](https://github.com/QwenLM) 微调而成，训练集体量 3k+ ，具有二次元女孩子的说话风格，比较傲娇，但乐于和你分享生活的琐碎，每天会给你不一样的问候。

# 功能🪄

✅ 支持近乎全自动安装环境

✅ 提供本人由 3k+ 对话数据微调的 ChatGLM2-6B P-Tuning V2 模型与 Qwen Lora 微调模型	

✅ 主动发起聊天（随机和每天早中晚固定时间）

✅ 提供 5 条命令以便在聊天中进行刷新回复等操作

✅ OFA 图像识别：识别表情包、理解表情包、发送表情包

✅ 支持通过 [fishaudio/fish-speech](https://github.com/fishaudio/fish-speech) 进行语言合成（沐雪 TTS 模型尚未发布）

✅ 在群聊中聊天（支持被 @ 回复或不被 @ 随机回复）

✅ 在控制台中实时语音对话（暂不支持打 QQ 语音）

✅ 多语言文档

✅ 常见 Q&A 指南

✅ 清晰的日志管理输出

⬜ (Pending) 对记忆模块进行优化，实现长期记忆与短期记忆

⬜ 更好的记忆存储


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
conda create --name Muice python=3.10.10 -y
conda activate Muice
pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

对于 GPU 用户，请额外执行

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

对于 GPU 用户，请确保您已配置好 cuda 环境。[参考链接](https://blog.csdn.net/chen565884393/article/details/127905428)

## 模型下载和加载

目前支持的基底模型如下表：

| 基底模型                                                     | 对应微调模型版本号                         | 对应 loader           | 额外依赖库                  |
| ------------------------------------------------------------ | ------------------------------------------ | --------------------------- | --------------------------- |
| [ChatGLM2-6B-Int4](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b-int4/summary) | 2.2-2.4                                    | transformers                        | cpm_kernels                 |
| [ChatGLM2-6B](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b/summary) | 2.0-2.3                                    | transformers                        |                             |
| [Qwen-7B-Chat-Int4](https://www.modelscope.cn/models/qwen/Qwen-7B-Chat-Int4/summary) | 2.3、2.6.2                                 | llmtuner                         | ~~llmtuner~~                |
| [Qwen2-1.5B-Instruct-GPTQ-Int4](https://www.modelscope.cn/models/qwen/Qwen2-1.5B-Instruct-GPTQ-Int4/summary) | 2.5.3                                      | llmtuner                              | ~~llmtuner~~                |
| [Qwen2.5-7B-Instruct-GPTQ-Int4](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4) | 2.7.1 | llmtuner | ~~llmtuner~~ |
| [RWKV(Seikaijyu微调)](https://huggingface.co/Seikaijyu)      | 参见 [HF](https://huggingface.co/Seikaijyu) | rwkv-api | （需要下载配置 RWKV-Runner） |

本项目的`requirements.txt`基于 `llmtuner` 环境要求搭建，因此我们建议使用 Qwen 系列模型，若选用 ChatGLM 系列模型，可能会导致环境错误。

微调模型下载：[Releases](https://github.com/Moemu/Muice-Chatbot/releases)

建议将基底模型与微调模型放入 `model` 文件夹中然后在配置文件中配置相应配置项（确保配置文件中的路径目录下存在多个模型文件而不是只有一个文件夹，部分微调模型由于疏忽还套了一层 `checkpoint-xxx` 文件夹）

本仓库目前支持如下模型加载方式：

1. 通过 API 加载
2. 通过 `transformers` 的`AutoTokenizer`, `AutoModel` 函数加载
3. 通过`llmtuner.chat`（`LLaMA-Factory`）的 `ChatModel` 类加载
4. 通过 `RWKV-Runner` 提供的 API 服务加载

在配置文件中可调整模型的加载方式：

```yaml
model:
  loader: llmtuner # 模型加载器 transformers/llmtuner/rwkv-api
  model_path: model/Qwen2.5-7B-Instruct-GPTQ-Int4 # 基底模型路径
  adapter_path: model/Muice-2.7.1-Qwen2.5-7B-Instruct-GPTQ-Int4-8e-4 # 微调模型路径
```

（若是 API / rwkv-api 加载，`model_name_or_path` 填写对应的 API 地址）

如果你没有合适的显卡，需要通过 CPU 加载模型或者需要加载量化模型，请安装并配置 `GCC` 环境，然后勾选 `openmp`。[参考链接](https://blog.csdn.net/m0_52985087/article/details/136480206?spm=1001.2014.3001.5501)

## Bot 服务配置

现以提供 OneBot 服务支持, 无需担心 gocq 的风控(喜)

本项目使用 [OneBot V11](https://github.com/botuniverse/onebot-11) 协议, 若您希望于 QQ 使用, 推荐参考 [LLOneBot](https://github.com/LLOneBot/LLOneBot) 使用 OneBot 服务

注：请在安装好 LLOneBot 后, 于设置中开启反向 WebSocket 服务, 填写 `ws://127.0.0.1:21050/ws/api`, 以正常运行

您也可以使用 [Lagrange.Core](https://github.com/LagrangeDev/Lagrange.Core) 以及 [~~OpenShamrock~~](https://github.com/whitechi73/OpenShamrock) 等来链接QQ, 或其他适配器链接其他软件，详见 [OneBot V11 适配器](https://onebot.dev/ecosystem.html#onebot-%E5%AE%9E%E7%8E%B0-1)

**能使用请勿随意更新 QQNT, 若无法使用请尝试降级 QQNT**

## 其他功能

- [语音回复](docs/other_func.md#语音回复)
- [图像识别（识别 / 发送表情包）](docs/other_func.md#ofa-图像识别识别--发送表情包)
- [Faiss 长期记忆](docs/other_func.md#faiss-长期记忆实验性内容)
- [实时语音聊天](docs/other_func.md#启动实时语音聊天)

# 配置⚒️

配置文件机器说明位于 `configs.yml`，请根据你的需求进行修改

2024.12.04更新：我们更新了配置文件格式，为了迎合即将到来的 2.7.x 模型，我们添加了如下配置项：

```yaml
# 主动对话相关
active:
  enable: false # 是否启用主动对话
  rate: 0.003 # 主动对话概率（每分钟）
  active_prompts:
    - '<生成推文: 胡思乱想>'
    - '<生成推文: AI生活>'
    - '<生成推文: AI思考>'
    - '<生成推文: 表达爱意>'
    - '<生成推文: 情感建议>'
  not_disturb: true # 是否开启免打扰模式
  shecdule:
    enable: true # 是否启用定时任务
    rate: 0.75 # 定时任务概率（每次）
    tasks:
      - hour: 8
        prompt: '<日常问候: 早上>'
      - hour: 12
        prompt: '<日常问候: 中午>'
      - hour: 18
        prompt: '<日常问候: 傍晚>'
      - hour: 22
        prompt: '<日常问候: 深夜>'
  targets: # 主动对话目标QQ号
    - 12345678
    - 23456789
```

如果你使用的是 2.7.x 之前的模型，请更改如下配置项：

```yaml
  active_prompts:
    - '（分享一下你的一些想法）'
    - '（创造一个新话题）'
```

以及：

```yaml
    tasks:
      - hour: 8
        prompt: '（发起一个早晨问候）'
      - hour: 12
        prompt: '（发起一个中午问候）'
      - hour: 18
        prompt: '（发起一个傍晚问候）'
      - hour: 22
        prompt: '（发起一个临睡问候）'
```

# 使用🎉

在本项目根目录下运行 `main.py`

```powershell
conda activate Muice
python main.py
```

或是运行自动安装脚本生成的启动脚本`start.bat`

# 命令🕹️

| 命令       | 释义                |
|----------|-------------------|
| /clean   | 清空本轮对话历史          |
| /refresh | 刷新本次对话            |
| /help    | 显示所有可用的命令列表       |
| /reset   | 重置所有对话数据(将存档对话数据) |
| /undo    | 撤销上一次对话           |

# 常见FAQ

[常见FAQ](./docs/faq.md) 

# 示例对话（训练集）📑

参见公开的训练集 [Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)

# 沐雪人设

与其他聊天机器人项目不同，本项目提供由本人通过自家对话数据集微调后的模型，在 Release 中提供下载，关于微调后的模型人设，目前公开的信息如下：

![沐雪人设图（若无法打开请通过右键打开）](https://i0.hdslb.com/bfs/new_dyn/9fc79347b54c5f2835884c8f755bd1ea97020216.png)

训练集开源地址： [Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)

原始模型：[THUDM/ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) & [QwenLM/Qwen](https://github.com/QwenLM/Qwen)）

本项目源码使用 [MIT License](https://github.com/Moemu/Muice-Chatbot/blob/main/LICENSE)，对于微调后的模型文件，不建议将其作为商业用途

# 关于🎗️

代码实现：[Moemu](https://github.com/Moemu)、[MoeSnowyFox](https://github.com/MoeSnowyFox)、[NaivG](https://github.com/NaivG)、[zkhssb](https://github.com/zkhssb)

训练集编写与模型微调：[Moemu](https://github.com/Moemu) （RWKV 微调：[Seikaijyu](https://github.com/Seikaijyu)）

帮助文档编写：[TurboHK](https://github.com/TurboHK)、[叶子](https://github.com/FHU-yezi)

> 友情连接：[Coral 框架](https://github.com/ProjectCoral/Coral)

总代码贡献：

<a href="https://github.com/eryajf/Moemu/Muice-Chatbot/contributors">
  <img src="https://contrib.rocks/image?repo=Moemu/Muice-Chatbot"  alt="图片加载中..."/>
</a>

如果此项目对你有帮助，您可以考虑赞助。

<a href="https://www.buymeacoffee.com/Moemu" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 45px !important;width: 163px !important;" ></a>

感谢你们所有人的支持！

本项目隶属于 Muice-Project。

Star History：

[![Star History Chart](https://api.star-history.com/svg?repos=Moemu/Muice-Chatbot&type=Date)](https://star-history.com/#Moemu/Muice-Chatbot&Date)

