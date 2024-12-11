![](../src/Cover.png)
<p style="text-align:center">
<img src="https://img.shields.io/github/stars/Moemu/Muice-Chatbot" alt="Stars">
<img src="https://img.shields.io/badge/Model-ChatGLM2--6B & Qwen--7B-green" alt="Model">
<img src="https://img.shields.io/badge/HuggingFace-Dataset-yellow?link=https%3A%2F%2Fhuggingface.co%2Fdatasets%2FMoemu%2FMuice-Dataset" alt="HuggingFace">
<img src="https://img.shields.io/badge/Python-3.10-blue" alt="Python">
</p>

[简体中文](../Readme.md) | [繁體中文](./Readme_tc.md)  | English | [日本語](.Readme_jp.md)

> [!IMPORTANT]
> As of 2024.12.04, due to a configuration format update, please reset your configuration file if you've fetched updates to this repository. We apologize for any inconvenience caused.

> [!WARNING]
> The chatbot is trained in Simplified Chinese, which may limit its ability to handle English input effectively. Let us know if you are interested in a version fine-tuned with a machine-translated dataset in English!

> [!TIP]
> This page's content might not always reflect the latest updates. Visit the Simplified Chinese page for the most recent information.

# Introduction ✨

Muice is an AI chatbot, who actively engages in conversation and is trained using over 3,000 dialogue samples. The chatbot features a conversational style resembling a cheerful anime girl who enjoys sharing daily life anecdotes and greets users with unique messages every day. It is fine-tuned on [ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) and [Qwen](https://github.com/QwenLM).

## Features 🪄

✅ **Automated Environment Setup**: Easy, nearly hands-free installation process.

✅**Fine-tuned Models Provided**: Provide ChatGLM2-6B P-Uni V2 model and Qwen Qlora fine-tuning model fine tuned by myself with 3k+conversation data

✅ **Scheduled and Random Conversations**: Automatically initiates chats at specific times of the day.

✅ **Command Support**: Includes five commands to refresh, reply, and manage conversations.

✅ **OFA Image Recognition**: Can recognize and send memes or stickers.

✅ **TTS Support**: Uses [fish-speech](https://github.com/fishaudio/fish-speech) for voice synthesis (custom TTS models are under development).

✅ **Multi-Language Support**: Comprehensive multilingual documentation.

⬜ Optimized memory modules for long-term and short-term memory capabilities.

⬜ Improved logging mechanisms with automated bug report generation.

⬜ Comprehensive FAQ guide.


## Getting Started 💻

### Recommended Environment:

- **Python**: Version 3.10+
- **Hardware**: A GPU with at least 6GB VRAM (4GB VRAM for int4 quantization, 16GB RAM for CPU inference).

### Automated Installation

Follow these steps for a quick setup:
1. Download and unzip the latest code from `Code -> Download ZIP`.
2. Run `install_env.bat` by double-clicking or using the following command:

```powershell
.\install_env.bat
```

Note: The script sets up a Python virtual environment, no Conda required.

### Manual Installation (Using Conda)

```powershell
git clone https://github.com/Moemu/Muice-Chatbot
cd Muice-Chatbot
conda create --name Muice python=3.10.10 -y
conda activate Muice
pip install -r requirements.txt
```

For GPU users:

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

Ensure CUDA is configured properly ( [Reference](https://blog.csdn.net/chen565884393/article/details/127905428) ).

## Model Download and Loading

Supported base models:

| Model                                                        | Fine-tuned Version                         | Extra Dependencies          |
| ------------------------------------------------------------ | ------------------------------------------ | --------------------------- |
| [ChatGLM2-6B-Int4](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b-int4/summary) | 2.2-2.4                                    | cpm_kernels                 |
| [ChatGLM2-6B](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b/summary) | 2.0-2.3                                    |                             |
| [Qwen-7B-Chat-Int4](https://www.modelscope.cn/models/qwen/Qwen-7B-Chat-Int4/summary) | 2.3、2.6.2                                 | llmtuner                    |
| [Qwen2-1.5B-Instruct-GPTQ-Int4](https://www.modelscope.cn/models/qwen/Qwen2-1.5B-Instruct-GPTQ-Int4/summary) | 2.5.3                                      | llmtuner                    |
| [Qwen2.5-7B-Instruct-GPTQ-Int4](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4) | 2.7.1                                      | llmtuner                    |
| [RWKV (By Seikaijyu)](https://huggingface.co/Seikaijyu)      | see [HF](https://huggingface.co/Seikaijyu) | （RWKV-Runner is required） |

Place the models in the `model` folder. Ensure fine-tuned models include a `.model` file.

Loading methods:

- Via API
- Using `transformers.AutoTokenizer` and `transformers.AutoModel`.
- Through `llmtuner.chat.ChatModel`.
- With `RWKV-Runner` APIs.

In the tested models, we recommend using the corresponding loading method for the following models, and other models can also be loaded using similar methods:

| Base model                   | Fine tuning method | Loading method |
| ---------------------------- | ------------------ | -------------- |
| ChatGLM                      | P-tuning V2        | transformers   |
| Qwen                         | sft                | llmtuner       |
| RWKV (Seikaijyu fine-tuning) | pissa              | rwkv apin      |

The model loading method can be adjusted in the configuration file:

```yaml
# model
model:
  loader: transformers # transformers/llmtuner/rwkv-api
  model_path: ./model/chatglm2-6b # base model path
  adapter_path: ./model/Muice # fine-tuning model path
```

(If loading for API / rwkv-api , fill in the corresponding API address for `model_name_or_path`)

If you do not have a suitable graphics card and need to load models or quantization models through the CPU, please install and configure the `GCC` environment and check `openmp`. [Reference link(ZH)]( https://blog.csdn.net/m0_52985087/article/details/136480206?spm=1001.2014.3001.5501)

## Bot Service Configuration ⚙️

This project supports the [OneBot V11 Protocol](https://github.com/botuniverse/onebot-11), enabling compatibility with QQ and other applications.

To connect with QQ:

1. Install [LLOneBot](https://github.com/LLOneBot/LLOneBot).
2. Enable reverse WebSocket and set it to `ws://127.0.0.1:21050/ws/api`.
3. Alternatively, use [Lagrange.Core](https://github.com/LagrangeDev/Lagrange.Core) or other adapters compatible with OneBot V11 ([Adapter List](https://onebot.dev/ecosystem.html#onebot-implementations)).

**Important**: Avoid upgrading QQNT unnecessarily. If issues arise, consider downgrading.


## Additional Features 🎨

- **Voice Reply**: Supports TTS replies. [Learn more(ZH)](./docs/other_func.md#voice-replies).
- **Image Recognition**: Handles meme recognition and response. [Details(ZH)](./docs/other_func.md#image-recognition).
- **Faiss Long-Term Memory**: Experimental long-term memory capability. [Documentation(ZH)](https://chatgpt.com/c/docs/other_func.md#faiss-memory).
- **Real-Time Voice Chat**: Allows for interactive voice communication. [Setup Guide(ZH)](https://chatgpt.com/c/docs/other_func.md#real-time-voice-chat).


## Project Structure Overview 🗂️

After completing setup, your directory should resemble the following:

```
Muice-Chatbot     <- Root directory
 ├─llm
 ├─model
 │  ├─ chatglm2-6b       <- Base model (select one)
 │  ├─ chatglm2-6b-int4  <- Int4 quantized model
 │  ├─ Qwen-7B-Chat-Int4 <- Qwen-7B-int4
 │  └─ Muice
 ├─configs.yml  <- Configuration file
 ├─ws.py         <- WebSocket service
 ├─main.py       <- Main application
 ├─requirements.txt
 └─...
```

---

## Configuration ⚒️

The configuration file is located in `configs.yml`. Adjust settings to match your requirements.

### Updates (Post-2024.12.04):

New configurations have been introduced for models versioned 2.7.x and above:

```yaml
# Active Conversations
active:
  enable: false  # Enable or disable active conversations
  rate: 0.003    # Probability of initiating a conversation (per minute)
  active_prompts:
    - '<生成推文: 胡思乱想>'
    - '<生成推文: AI生活>'
    - '<生成推文: AI思考>'
    - '<生成推文: 表达爱意>'
    - '<生成推文: 情感建议>'
  not_disturb: true  # Enable Do Not Disturb mode
  schedule:
    enable: true  # Enable scheduled tasks
    rate: 0.75    # Probability of executing scheduled tasks
    tasks:
      - hour: 8
        prompt: '<日常问候: 早上>'
      - hour: 12
        prompt: '<日常问候: 中午>'
      - hour: 18
        prompt: '<日常问候: 傍晚>'
      - hour: 22
        prompt: '<日常问候: 深夜>'
  targets:  # List of QQ IDs for active conversations
    - 12345678
    - 23456789

```

For pre-2.7.x models, use the following configuration format instead:

```yaml
  active_prompts:
    - '（分享一下你的一些想法）'
    - '（创造一个新话题）'
```

And:

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

## Usage 🎉

Run the main application from the project root directory:

```powershell
conda activate Muice
python main.py
```

Alternatively, use the generated `start.bat` script.

------

## Commands 🕹️

| Command  | Description                            |
| -------- | -------------------------------------- |
| /clean   | Clear the current conversation history |
| /refresh | Refresh the current conversation       |
| /help    | Display all available commands         |
| /reset   | Reset all conversation data            |
| /undo    | Undo the last conversation entry       |

------

## Example Conversations (Training Data) 📑

View the public dataset: [Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset).

------

## Character Design 🎨

Unlike other chatbot projects, this project provides a model that I have fine tuned based on my own conversation dataset, which can be downloaded in the Release. The publicly available information regarding the fine tuned model persona is as follows:

![Muice Character Design](https://i0.hdslb.com/bfs/new_dyn/9fc79347b54c5f2835884c8f755bd1ea97020216.png)

Training set open source address: [Moemu/Muice-Dataset]( https://huggingface.co/datasets/Moemu/Muice-Dataset )

Original model: [THUDM/ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) & [QwenLM/Qwen](https://github.com/QwenLM/Qwen)

The source code of this project uses [MIT License]（ https://github.com/Moemu/Muice-Chatbot/blob/main/LICENSE ）For fine tuned model files, it is not recommended to use them for commercial purposes.

## About🎗️

- **Code Implementation**: [Moemu](https://github.com/Moemu), [MoeSnowyFox](https://github.com/MoeSnowyFox), [NaivG](https://github.com/NaivG), [zkhssb](https://github.com/zkhssb).
- **Dataset Creation and Model Tuning**: [Moemu](https://github.com/Moemu), RWKV fine-tuning by [Seikaijyu](https://github.com/Seikaijyu).
- **Documentation**: [TurboHK](https://github.com/TurboHK), [FHU-yezi](https://github.com/FHU-yezi).

> **Friendship Link: **[Coral](https://github.com/ProjectCoral/Coral)

All contributors:

<a href="https://github.com/eryajf/Moemu/Muice-Chatbot/contributors">
  <img src="https://contrib.rocks/image?repo=Moemu/Muice-Chatbot"  alt="Loading..."/></a>

If you find this project helpful, consider supporting it:

<a href="https://www.buymeacoffee.com/Moemu" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 45px !important;width: 163px !important;" ></a>

Thanks you all!

**Star History:**

[![Star History Chart](https://api.star-history.com/svg?repos=Moemu/Muice-Chatbot&type=Date)](https://star-history.com/#Moemu/Muice-Chatbot&Date)

