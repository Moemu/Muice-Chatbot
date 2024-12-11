![](../src/Cover.png)
<p style="text-align:center">
<img src="https://img.shields.io/github/stars/Moemu/Muice-Chatbot" alt="Stars">
<img src="https://img.shields.io/badge/Model-ChatGLM2--6B & Qwen--7B-green" alt="Model">
<img src="https://img.shields.io/badge/HuggingFace-Dataset-yellow?link=https%3A%2F%2Fhuggingface.co%2Fdatasets%2FMoemu%2FMuice-Dataset" alt="HuggingFace">
<img src="https://img.shields.io/badge/Python-3.10-blue" alt="Python">
</p>

[简体中文](../Readme.md) | 繁體中文 | [English](./Readme_en.md) | [日本語](.Readme_jp.md)

> [!IMPORTANT]
> 2024.12.04 更新：由於配置文件格式變更，若您曾拉取過本 Repo 並於 12.04 後執行過 fetch 操作，請重新設定配置文件，對此帶來的不便我們深感抱歉。

> [!WARNING]
> 我們使用簡體中文進行訓練，所以可能模型難以回答由繁體中文組成的問題。
如果你需要由機器翻譯後的繁體中文訓練集微調後的模型，歡迎告訴我！

> [!TIP]
> 此頁面的內容可能不是最新的，我們將不定時更新此頁面的內容，若要獲取最新更新，請轉自簡體中文頁面。

# 介紹✨

沐雪，一個會**主動**找您聊天的 AI 女孩，其對話模型基於 [ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) 與 [Qwen](https://github.com/QwenLM) 微調而成，訓練集規模 3k+，具有二次元女孩的說話風格，稍顯傲嬌，但樂於與您分享生活瑣事，每天會送上不一樣的問候。

# 功能🪄

✅ 支援幾乎全自動安裝環境

✅ 提供由本人以 3k+ 對話數據微調的 ChatGLM2-6B P-Tuning V2 模型與 Qwen Qlora 微調模型	

✅ 主動發起聊天（隨機及每天早中晚固定時間）

✅ 提供 5 條指令以便在聊天中進行刷新、回覆等操作

✅ OFA 圖像識別：識別表情包、理解表情包、發送表情包

✅ 支援通過 [fishaudio/fish-speech](https://github.com/fishaudio/fish-speech) 進行語音合成（沐雪 TTS 模型尚未發布）

✅ 在群聊中聊天（支援被 @ 回覆或不被 @ 隨機回覆）

✅ 在控制台中即時對話（暫不支援 QQ 語音）

✅ 提供多語言文檔

⬜ 優化記憶模組，實現長期記憶與短期記憶

⬜ 完善日誌記錄機制，實現自動生成 bug 報告

⬜ 建立常見 Q&A 指南

# 快速開始💻

建議環境：

- Python 3.10+
- 一張擁有 6GB 或以上顯存的顯卡（int4 量化最低要求為 4G 顯存，CPU 推理需要 16G 或以上內存）

## 自動安裝

目前已實現自動安裝所有軟件與依賴。通過 `Code -> Download ZIP` 下載並解壓最新源碼。

雙擊 `install_env.bat` 安裝（**請勿啟用舊版控制台**），或在命令行中執行以下命令：

```powershell
.\install_env.bat
```

自動安裝可能需要較長時間，請耐心等待，安裝完成後，您仍需手動下載模型。

**自動安裝腳本使用的是 Python 虛擬環境，不需要 Conda，請留意安裝腳本的提示。**

## 手動安裝（使用 Conda）

```powershell
git clone https://github.com/Moemu/Muice-Chatbot
cd Muice-Chatbot
conda create --name Muice python=3.10.10 -y
conda activate Muice
pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

GPU 用戶需額外執行：

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

GPU 用戶請確保已配置好 CUDA 環境。[參考連結](https://blog.csdn.net/chen565884393/article/details/127905428)

## 模型下載與加載

目前支援的基底模型如下表：

| 基底模型                                                     | 對應微調模型版本號                        | 額外依賴庫                 |
| ------------------------------------------------------------ | ----------------------------------------- | -------------------------- |
| [ChatGLM2-6B-Int4](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b-int4/summary) | 2.2-2.4                                   | cpm_kernels                |
| [ChatGLM2-6B](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b/summary) | 2.0-2.3                                   |                            |
| [Qwen-7B-Chat-Int4](https://www.modelscope.cn/models/qwen/Qwen-7B-Chat-Int4/summary) | 2.3、2.6.2                                | llmtuner                   |
| [Qwen2-1.5B-Instruct-GPTQ-Int4](https://www.modelscope.cn/models/qwen/Qwen2-1.5B-Instruct-GPTQ-Int4/summary) | 2.5.3                                     | llmtuner                   |
| [Qwen2.5-7B-Instruct-GPTQ-Int4](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4) | 2.7.1                                     | llmtuner                   |
| [RWKV(Seikaijyu 微調)](https://huggingface.co/Seikaijyu)     | 見 [HF](https://huggingface.co/Seikaijyu) | （需下載配置 RWKV-Runner） |

微調模型下載：[Releases](https://github.com/Moemu/Muice-Chatbot/releases)

將基底模型與微調模型放入 `model` 文件夾中（確保微調模型目錄下存在 `.model` 文件而非文件夾，部分微調模型因疏忽還多了一層 `checkpoint` 文件夾）。

本倉庫目前支援以下模型加載方式： 

1. 通過 API 加載 
2. 通過 `transformers` 的 `AutoTokenizer`, `AutoModel` 函數加載
3. 通過 `llmtuner.chat`（`LLaMA-Factory`）的 `ChatModel` 類加載
4. 通過 `RWKV-Runner` 提供的 API 服務加載

在已測試的模型中，我們建議以下模型使用對應方式加載，其它模型亦可採用類似方法加載： 

| 基底模型              | 微調方式        | 加載方法         |
|-------------------|-------------|--------------|
| ChatGLM           | P-tuning V2 | transformers |
| Qwen              | sft         | llmtuner     |
| RWKV（Seikaijyu 微調） | pissa       | rwkv-api     |

在配置文件中可調整模型加載方式：

```yaml
# 模型相關
model:
  loader: transformers # 模型加載器 transformers/llmtuner/rwkv-api
  model_path: ./model/chatglm2-6b # 基底模型路徑
  adapter_path: ./model/Muice # 微調模型路徑
```

（若為 API / rwkv-api 加載，`model_name_or_path` 填寫對應的 API 地址）

若您沒有合適的顯卡，需要通過 CPU 加載模型或加載量化模型，請安裝並配置 `GCC` 環境，並勾選 `openmp`。[參考連結](https://blog.csdn.net/m0_52985087/article/details/136480206?spm=1001.2014.3001.5501)

## Bot 服務配置

目前提供 OneBot 服務支持，無需擔心 gocq 的風控。

本項目使用 [OneBot V11](https://github.com/botuniverse/onebot-11) 協議，若希望於 QQ 上使用，建議參考 [LLOneBot](https://github.com/LLOneBot/LLOneBot) 配置 OneBot 服務。

**注意：請在安裝好 LLOneBot 後，於設置中開啟反向 WebSocket 服務，並填寫 `ws://127.0.0.1:21050/ws/api`，以正常運行。**

您也可以使用 [Lagrange.Core](https://github.com/LagrangeDev/Lagrange.Core) 或 [~~OpenShamrock~~](https://github.com/whitechi73/OpenShamrock) 等來連接 QQ，或其他適配器連接其他軟件。詳情見 [OneBot V11 適配器](https://onebot.dev/ecosystem.html#onebot-实现-1)。

**請勿隨意升級 QQNT；若出現無法使用情況，請嘗試降級 QQNT。**

## 其他功能

- [語音回覆](https://chatgpt.com/c/docs/other_func.md#語音回覆)
- [圖像識別（識別 / 發送表情包）](https://chatgpt.com/c/docs/other_func.md#ofa-圖像識別識別--發送表情包)
- [Faiss 長期記憶](https://chatgpt.com/c/docs/other_func.md#faiss-長期記憶實驗性內容)
- [實時語音聊天](https://chatgpt.com/c/docs/other_func.md#啟動實時語音聊天)

## 總結

完成上述操作後，您的項目文件結構應如下所示：

```
Muice-Chatbot     <- 主目錄
 ├─llm
 ├─model
 │  ├─ chatglm2-6b       <- 原始模型（選其一）
 │  ├─ chatglm2-6b-int4  <- int4 原始模型
 │  ├─ Qwen-7B-Chat-Int4 <- Qwen-7B-int4 原始模型
 │  └─ Muice
 ├─configs.yml  <- 配置文件
 ├─ws.py         <- ws 服務
 ├─main.py       <- 主程序
 ├─requirements.txt
 └─...
```

# 配置⚒️

配置文件位於 `configs.yml`，請根據您的需求進行修改。

2024.12.04 更新：配置文件格式已更新，為迎合即將到來的 2.7.x 模型，新增以下配置項：

```yaml
# 主動對話相關
active:
  enable: false # 是否啟用主動對話
  rate: 0.003 # 主動對話概率（每分鐘）
  active_prompts:
    - '<生成推文: 胡思乱想>'
    - '<生成推文: AI生活>'
    - '<生成推文: AI思考>'
    - '<生成推文: 表达爱意>'
    - '<生成推文: 情感建议>'
  not_disturb: true # 是否開啟免打擾模式
  shecdule:
    enable: true # 是否啟用定時任務
    rate: 0.75 # 定時任務概率（每次）
    tasks:
      - hour: 8
        prompt: '<日常问候: 早上>'
      - hour: 12
        prompt: '<日常问候: 中午>'
      - hour: 18
        prompt: '<日常问候: 傍晚>'
      - hour: 22
        prompt: '<日常问候: 深夜>'
  targets: # 主動對話目標 QQ 號
    - 12345678
    - 23456789
```

若使用的是 2.7.x 之前的模型，請改為以下配置：

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

在本項目根目錄下運行 `main.py`：

```powershell
conda activate Muice
python main.py
```

或者運行自動安裝腳本生成的啟動腳本 `start.bat`。

# 命令🕹️

| 命令     | 含義                               |
| -------- | ---------------------------------- |
| /clean   | 清空本輪對話歷史                   |
| /refresh | 刷新本次對話                       |
| /help    | 顯示所有可用的命令列表             |
| /reset   | 重置所有對話數據（將存檔對話數據） |
| /undo    | 撤銷上一次對話                     |

# 示例對話（訓練集）📑

參見公開的訓練集 [Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)

# 沐雪人設

與其他聊天機器人項目不同，本項目提供了由本人基於自家對話數據集微調後的模型，可在 Release 中下載。關於微調後的模型人設，目前公開的信息如下：

![沐雪人設圖（若無法打開請右鍵打開）](https://i0.hdslb.com/bfs/new_dyn/9fc79347b54c5f2835884c8f755bd1ea97020216.png)

訓練集開源地址：[Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)

原始模型：[THUDM/ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) 與 [QwenLM/Qwen](https://github.com/QwenLM/Qwen)

本項目源碼使用 [MIT License](https://github.com/Moemu/Muice-Chatbot/blob/main/LICENSE)，對於微調後的模型文件，不建議將其用於商業用途。

# 關於🎗️

**代碼實現：**[Moemu](https://github.com/Moemu)、[MoeSnowyFox](https://github.com/MoeSnowyFox)、[NaivG](https://github.com/NaivG)、[zkhssb](https://github.com/zkhssb)

**訓練集編寫與模型微調：**[Moemu](https://github.com/Moemu)（RWKV 微調：[Seikaijyu](https://github.com/Seikaijyu)）

**幫助文檔編寫：**[TurboHK](https://github.com/TurboHK)、[叶子](https://github.com/FHU-yezi)

> **友情連結：**[Coral 框架](https://github.com/ProjectCoral/Coral)

總代碼貢獻：

<a href="https://github.com/eryajf/Moemu/Muice-Chatbot/contributors">
  <img src="https://contrib.rocks/image?repo=Moemu/Muice-Chatbot"  alt="Loading..."/>

如果此項目對您有幫助，歡迎考慮贊助：

<a href="https://www.buymeacoffee.com/Moemu" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 45px !important;width: 163px !important;" ></a>

感謝您們所有人的支持！

**Star History：**

[![Star History Chart](https://api.star-history.com/svg?repos=Moemu/Muice-Chatbot&type=Date)](https://star-history.com/#Moemu/Muice-Chatbot&Date)