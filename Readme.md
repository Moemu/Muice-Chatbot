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

⬜ 对记忆模块进行优化，实现长期记忆与短期记忆

⬜ 完善日志记录机制，实现自动生成 bug 报告

⬜ 建立常见 Q&A 指南

⬜ 提供多语言文档


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

如果你没有合适的显卡，需要通过 CPU 加载模型，请安装并配置 `GCC` 环境，然后勾选 `openmp`。[参考链接](https://blog.csdn.net/m0_52985087/article/details/136480206?spm=1001.2014.3001.5501)

## Bot 服务配置

现以提供 OneBot 服务支持, 无需担心 gocq 的风控(喜)

本项目使用 [OneBot V11](https://github.com/botuniverse/onebot-11) 协议, 若您希望于 QQ 使用, 推荐参考 [LLOneBot](https://github.com/LLOneBot/LLOneBot) 使用 OneBot 服务

注：请在安装好 LLOneBot 后, 于设置中开启反向 WebSocket 服务, 填写 `ws://127.0.0.1:21050/ws/api`, 以正常运行

您也可以使用 [Lagrange.Core](https://github.com/LagrangeDev/Lagrange.Core) 以及 [~~OpenShamrock~~](https://github.com/whitechi73/OpenShamrock) 等来链接QQ, 或其他适配器链接其他软件，详见 [OneBot V11 适配器](https://onebot.dev/ecosystem.html#onebot-%E5%AE%9E%E7%8E%B0-1)

**能使用请勿随意更新 QQNT, 若无法使用请尝试降级 QQNT**

## 其他功能

- [语音回复](docs/other_func.md#语音回复)
- [图像识别（识别 / 发送表情包）](docs/other_func.md##ofa-图像识别识别--发送表情包)
- [Faiss 长期记忆](docs/other_func.md#faiss-长期记忆实验性内容)
- [实时语音聊天](docs/other_func.md#启动实时语音聊天)

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

配置文件位于 `config.json`，请根据你的需求进行修改（具体参考[配置说明](docs/config.md)）。

你也可以使用`configuration_gui.py`图形化界面配置文件。

```powershell
python configuration_gui.py
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

如果此项目对你有帮助，您可以考虑赞助。按照沐雪赞助使用方法，所有收入将抽取20%用于慈善事业（提供证书）。

<a href="https://www.buymeacoffee.com/Moemu" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 45px !important;width: 163px !important;" ></a>

感谢你们所有人的支持！无论你是否赞助和贡献代码！

Star History：

[![Star History Chart](https://api.star-history.com/svg?repos=Moemu/Muice-Chatbot&type=Date)](https://star-history.com/#Moemu/Muice-Chatbot&Date)

