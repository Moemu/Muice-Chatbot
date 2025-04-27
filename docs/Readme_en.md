![](src/Cover.png)
<p style="text-align:center">
<img src="https://img.shields.io/github/stars/Moemu/Muice-Chatbot" alt="Stars">
<img src="https://img.shields.io/badge/Model-ChatGLM2--6B & Qwen--7B-green" alt="Model">
<img src="https://img.shields.io/badge/HuggingFace-Dataset-yellow?link=https%3A%2F%2Fhuggingface.co%2Fdatasets%2FMoemu%2FMuice-Dataset" alt="HuggingFace">
<img src="https://img.shields.io/badge/Python-3.10-blue" alt="Python">
<a href='https://pd.qq.com/s/d4n2xp45i'><img src="https://img.shields.io/badge/QQ频道-沐雪的小屋-blue" alt="Stars"></a>
</p>

[简体中文](../Readme.md) | [繁體中文](./Readme_tc.md)  | English | [日本語](./Readme_jp.md)

> [!CAUTION]  
>  
> Muice-Chatbot has officially ceased updates as of February 19, 2025, and will enter archive status on July 16, 2025.  
>  
> Therefore, we strongly recommend migrating to [the MuiceBot framework based on Nonebot2](https://github.com/Moemu/MuiceBot). For migration instructions, please refer to: [Migrating from Muice-Chatbot](https://bot.snowy.moe/guide/migrations)  

> [!WARNING]
> The chatbot is trained in Simplified Chinese, which may limit its ability to handle English input effectively. Let us know if you are interested in a version fine-tuned with a machine-translated dataset in English!

> [!TIP]
> This page's content might not always reflect the latest updates. Visit the Simplified Chinese page for the most recent information.

# Introduction ✨  

Muice, an AI girl who **actively** initiates conversations with you. Her dialogue model is fine-tuned based on [Qwen](https://github.com/QwenLM), trained on a dataset of 3k+ dialogues. She embodies the speech style of an anime girl—somewhat tsundere but eager to share life's trivialities with you, offering unique greetings every day.  

# Features 🪄  

✅ Supports nearly fully automated environment setup.  

✅ Provides a Qwen LoRA fine-tuned model trained on 3k+ dialogues.  

✅ Supports multiple model loaders, allowing use without Muice's fine-tuned model.  

✅ Initiates conversations actively (randomly or at fixed times in the morning, noon, and evening).  

✅ Offers 5 commands for refreshing replies and other operations during chats.  

✅ OFA image recognition: Identifies memes, understands memes, and sends memes.  

✅ Supports speech synthesis via [fishaudio/fish-speech](https://github.com/fishaudio/fish-speech) (Muice TTS model not yet released).  

✅ Engages in group chats (supports replying when @mentioned or randomly without @mention).  

✅ Real-time voice conversations in the console (QQ voice calls not yet supported).  

✅ Multilingual documentation.  

✅ Common Q&A guide.  

✅ Clear log management output.  

✅ Faiss memory module: Retrieves past dialogue data and automatically adds it to the context.  

# Quick Start 💻  

Recommended environment:  

- Python 3.10  
- A GPU with 6GB+ VRAM (int4 quantization requires at least 4GB VRAM; CPU inference requires 16GB+ RAM).  

## Automatic Installation (venv)  

The setup now automates the installation of all software and dependencies. Download the latest source code via `Code -> Download ZIP` and extract it.  

Double-click `install_env.bat` to install (**do not enable legacy console**), or run the following command in the terminal:  

```powershell  
.\install_env.bat  
```  

The automatic installation may take some time. After completion, you still need to manually download the model.  

**The automatic installation script uses Python virtual environments and does not require Conda. Pay attention to the script's prompts.**  

## Manual Installation (Using Conda)  

```powershell  
git clone https://github.com/Moemu/Muice-Chatbot  
cd Muice-Chatbot  
conda create --name Muice python=3.10.10 -y  
conda activate Muice  
pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple  
```  

For GPU users, additionally run:  

```powershell  
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124  
```  

For GPU users, ensure your CUDA environment is configured. [Reference link](https://blog.csdn.net/chen565884393/article/details/127905428).  

## Loading Muice's Fine-Tuned Model  

Currently supported base models are listed below:  

| Base Model | Corresponding Fine-Tuned Model Version | Loader | Additional Dependencies |  
|------------|----------------------------------------|--------|-------------------------|  
| [ChatGLM2-6B-Int4](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b-int4/summary) | 2.2-2.4 | transformers | cpm_kernels |  
| [ChatGLM2-6B](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b/summary) | 2.0-2.3 | transformers | - |  
| [Qwen-7B-Chat-Int4](https://www.modelscope.cn/models/qwen/Qwen-7B-Chat-Int4/summary) | 2.3, 2.6.2 | llmtuner | ~~llmtuner~~ |  
| [Qwen2-1.5B-Instruct-GPTQ-Int4](https://www.modelscope.cn/models/qwen/Qwen2-1.5B-Instruct-GPTQ-Int4/summary) | 2.5.3 | llmtuner | ~~llmtuner~~ |  
| [Qwen2.5-7B-Instruct-GPTQ-Int4](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4) | 2.7.1 | llmtuner | ~~llmtuner~~ |  
| [RWKV (Fine-tuned by Seikaijyu)](https://huggingface.co/Seikaijyu) | See [HF](https://huggingface.co/Seikaijyu) | rwkv-api | (Requires RWKV-Runner setup) |  

The `requirements.txt` in this project is based on the `llmtuner` environment. Therefore, we recommend using the Qwen series models. Using ChatGLM series models may cause environment errors.  

Download fine-tuned models: [Releases](https://github.com/Moemu/Muice-Chatbot/releases)  

Place the base model and fine-tuned model in the `model` folder, then configure the corresponding settings in the configuration file (ensure the path in the configuration file points to multiple model files, not just a folder; some fine-tuned models may have an additional `checkpoint-xxx` folder).  

For Muice's Qwen fine-tuned models, the recommended configuration is:  

```yaml  
model:  
  loader: llmtuner  
  model_path: model/Qwen2.5-7B-Instruct-GPTQ-Int4 # Base model path  
  adapter_path: model/Muice-2.7.1-Qwen2.5-7B-Instruct-GPTQ-Int4-8e-4 # Fine-tuned model path  
  template: qwen # Model template in LLaMA-Factory (required)  
  system_prompt: 'Now you are an AI girl named "Muice"' # System prompt (optional)  
  auto_system_prompt: true # Automatically configure Muice's system prompt (default: false)  
```  

If you lack a suitable GPU and need to load the model on CPU or a quantized model, install and configure the `GCC` environment, then enable `openmp`. [Reference link](https://blog.csdn.net/m0_52985087/article/details/136480206?spm=1001.2014.3001.5501).  

## Using Without Muice's Fine-Tuned Model  

This repository also supports using other fine-tuned models or base models directly. Refer to [Supported Model Loaders](./docs/model.md) for configuration.  

Multimodal models are also supported. Refer to [Multimodal Model Loaders](./docs/model.md#multimodal-model-loader-configuration).  

## Bot Service Configuration  

OneBot service is now supported.  

This project uses the [OneBot V11](https://github.com/botuniverse/onebot-11) protocol. For QQ usage, we recommend [LLOneBot](https://github.com/LLOneBot/LLOneBot) or [Lagrange.Core](https://github.com/LagrangeDev/Lagrange.Core).  

For LLOneBot: After installation, enable the reverse WebSocket service in settings and enter `ws://127.0.0.1:21050/ws/api`.  

For Lagrange.Core: Follow [Lagrange Quick Deployment](https://lagrangedev.github.io/Lagrange.Doc/Lagrange.OneBot/Config/) and add the following configuration to its file:  

```json  
{  
	"Type": "ReverseWebSocket",  
	"Host": "127.0.0.1",  
	"Port": 21050,  
	"Suffix": "/ws/api",  
	"ReconnectInterval": 5000,  
	"HeartBeatInterval": 5000,  
	"HeartBeatEnable": true,  
	"AccessToken": ""  
}  
```  

Other OneBot V11 adapters can also be used. See [OneBot V11 Adapters](https://onebot.dev/ecosystem.html#onebot-%E5%AE%9E%E7%8E%B0-1).  

**Avoid updating QQNT unnecessarily. If issues arise, try downgrading QQNT.**  

> [!CAUTION]  
>  
> Update as of February 22, 2025: LiteLoaderQQNT-related account bans remain unresolved. To continue using it, downgrade QQNT to version `9.9.15-2xxxx`, install the framework, log in once, and immediately close it. Modify the following files in the root directory:  
>  
> `\resources\app-update.yml` -> `provider: 3rdparty`  
>  
> `\resources\app\versions\channel.json` -> `"channel": "bbbbbbbbbbeta"`  
>  
> Set these files to read-only to prevent QQNT from auto-updating.  

For Telegram Bot usage: [Migrate to Telegram Bot](./docs/telegram.md)  

## Other Features  

- [Voice Replies](docs/other_func.md#voice-replies)  
- [Image Recognition (Identify/Send Memes)](docs/other_func.md#ofa-image-recognition-identify--send-memes)  
- [Faiss Long-Term Memory (Experimental)](docs/other_func.md#faiss-long-term-memory-experimental)  
- [Real-Time Voice Chat](docs/other_func.md#start-real-time-voice-chat)  

# Configuration ⚒️  

Configuration file instructions are located in `configs.yml`. Modify them according to your needs.  

# Usage 🎉  

Run `main.py` in the project root directory:  

```powershell  
conda activate Muice  
python main.py  
```  

Or use the `start.bat` script generated by the automatic installation.  

# Commands 🕹️  

| Command | Description |  
|---------|-------------|  
| /clean | Clear current dialogue history. |  
| /refresh | Refresh the current dialogue. |  
| /help | Display all available commands. |  
| /reset | Reset all dialogue data (archives dialogue data). |  
| /undo | Undo the last dialogue. |  

# FAQ  

[FAQ](./docs/faq.md)  

# Example Dialogues (Training Dataset) 📑  

See the public dataset: [Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)  

# Muice's Character  

Unlike other chatbot projects, this project provides a model fine-tuned on a custom dialogue dataset, available for download in Releases. For details about the fine-tuned model's character, the currently public information is as follows:  

![Muice's Character Image (Right-click to open if unavailable)](https://i0.hdslb.com/bfs/new_dyn/9fc79347b54c5f2835884c8f755bd1ea97020216.png)  

Training dataset: [Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)  

Base models: [THUDM/ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) & [QwenLM/Qwen](https://github.com/QwenLM/Qwen))  

This project's source code uses the [MIT License](https://github.com/Moemu/Muice-Chatbot/blob/main/LICENSE). Commercial use of the fine-tuned model files is discouraged.  

# About 🎗️  

Code Implementation: [Moemu](https://github.com/Moemu), [MoeSnowyFox](https://github.com/MoeSnowyFox), [NaivG](https://github.com/NaivG), [zkhssb](https://github.com/zkhssb), [Asankilp](https://github.com/Asankilp)  

Dataset Creation and Model Fine-Tuning: [Moemu](https://github.com/Moemu) (RWKV fine-tuning: [Seikaijyu](https://github.com/Seikaijyu))  

Documentation: [TurboHK](https://github.com/TurboHK), [Leaf](https://github.com/FHU-yezi)  

> Related Projects: [Coral Framework](https://github.com/ProjectCoral/Coral), [nonebot-plugin-marshoai](https://github.com/LiteyukiStudio/nonebot-plugin-marshoai)  

Code Contributions:  

<a href="https://github.com/eryajf/Moemu/Muice-Chatbot/contributors">  
  <img src="https://contrib.rocks/image?repo=Moemu/Muice-Chatbot" alt="contributors"/>  
</a>  

If this project is helpful, consider supporting it.  

<a href="https://www.afdian.com/a/Moemu" target="_blank"><img src="https://pic1.afdiancdn.com/static/img/welcome/button-sponsorme.png" alt="afadian" style="height: 45px !important;width: 163px !important;"></a>  
<a href="https://www.buymeacoffee.com/Moemu" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 45px !important;width: 163px !important;" ></a>  

Thank you for your support!  

This project is part of MuikaAI.  

Official Channel: [Muice's Room](https://pd.qq.com/s/d4n2xp45i)  

Star History:  

[![Star History Chart](https://api.star-history.com/svg?repos=Moemu/Muice-Chatbot&type=Date)](https://star-history.com/#Moemu/Muice-Chatbot&Date)  