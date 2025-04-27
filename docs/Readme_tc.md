![](src/Cover.png)  
<p style="text-align:center">  
<img src="https://img.shields.io/github/stars/Moemu/Muice-Chatbot" alt="Stars">  
<img src="https://img.shields.io/badge/Model-ChatGLM2--6B & Qwen--7B-green" alt="Model">  
<img src="https://img.shields.io/badge/HuggingFace-Dataset-yellow?link=https%3A%2F%2Fhuggingface.co%2Fdatasets%2FMoemu%2FMuice-Dataset" alt="HuggingFace">  
<img src="https://img.shields.io/badge/Python-3.10-blue" alt="Python">  
<a href='https://pd.qq.com/s/d4n2xp45i'><img src="https://img.shields.io/badge/QQ频道-沐雪的小屋-blue" alt="Stars"></a>  
</p>  

[简体中文](../Readme.md) | 繁體中文 | [English](./Readme_en.md) | [日本語](./Readme_jp.md)

> [!CAUTION]  
>  
> Muice-Chatbot 已於 2025 年 2 月 19 日正式停止更新，並將於 2025 年 7 月 16 日進入歸檔狀態。  
>  
> 因此我們強烈建議您遷移至 [基於 Nonebot2 實現的 MuiceBot 框架](https://github.com/Moemu/MuiceBot) 中，有關遷移說明，請參考: [從 Muice-Chatbot 中遷移](https://bot.snowy.moe/guide/migrations)  

> [!WARNING]
> 我們使用簡體中文進行訓練，所以可能模型難以回答由繁體中文組成的問題。
> 如果你需要由機器翻譯後的繁體中文訓練集微調後的模型，歡迎告訴我！

> [!TIP]
> 此頁面的內容可能不是最新的，我們將不定時更新此頁面的內容，若要獲取最新更新，請轉自簡體中文頁面。

# 介紹 ✨  

沐雪，一隻會**主動**找你聊天的 AI 女孩子，其對話模型基於 [Qwen](https://github.com/QwenLM) 微調而成，訓練集體量 3k+ ，具有二次元女孩子的說話風格，比較傲嬌，但樂於和你分享生活的瑣碎，每天會給你不一樣的問候。  

# 功能 🪄  

✅ 支援近乎全自動安裝環境  

✅ 提供本人由 3k+ 對話數據微調的 Qwen Lora 微調模型  

✅ 支援多個模型加載器，可脫離沐雪微調模型使用  

✅ 主動發起聊天（隨機和每天早中晚固定時間）  

✅ 提供 5 條命令以便在聊天中進行刷新回覆等操作  

✅ OFA 圖像識別：識別表情包、理解表情包、發送表情包  

✅ 支援通過 [fishaudio/fish-speech](https://github.com/fishaudio/fish-speech) 進行語言合成（沐雪 TTS 模型尚未發佈）  

✅ 在群聊中聊天（支援被 @ 回覆或不被 @ 隨機回覆）  

✅ 在控制台中實時語音對話（暫不支援打 QQ 語音）  

✅ 多語言文檔  

✅ 常見 Q&A 指南  

✅ 清晰的日誌管理輸出  

✅ Faiss 記憶模組，從過去的對話數據中進行檢索並自動加入上下文  

# 快速開始 💻  

建議環境：  

- Python 3.10  
- 一張擁有 6GB 及以上顯存的顯卡（int4 量化最低要求為 4G 顯存，CPU 推理需要 16G 及以上記憶體）  

## 自動安裝（venv）  

目前已做到自動安裝所有軟體、依賴，通過 `Code -> Download ZIP` 下載解壓最新源碼。  

雙擊 `install_env.bat` 安裝（**不能啟用舊版控制台**），或在命令行中運行以下命令：  

```powershell  
.\install_env.bat  
```  

自動安裝可能需要較長時間，請耐心等待，安裝完成後，你仍需手動下載模型。  

**自動安裝腳本使用的是 Python 虛擬環境，不需要 Conda，請留意安裝腳本的提示。**  

## 手動安裝（使用 Conda）  

```powershell  
git clone https://github.com/Moemu/Muice-Chatbot  
cd Muice-Chatbot  
conda create --name Muice python=3.10.10 -y  
conda activate Muice  
pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple  
```  

對於 GPU 用戶，請額外執行  

```powershell  
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124  
```  

對於 GPU 用戶，請確保您已配置好 cuda 環境。[參考連結](https://blog.csdn.net/chen565884393/article/details/127905428)  

## 加載沐雪微調模型  

目前支援的基底模型如下表：  

| 基底模型 | 對應微調模型版本號 | 對應 loader | 額外依賴庫 |  
|------------|----------------|------------|------------|  
| [ChatGLM2-6B-Int4](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b-int4/summary) | 2.2-2.4 | transformers | cpm_kernels |  
| [ChatGLM2-6B](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b/summary) | 2.0-2.3 | transformers | - |  
| [Qwen-7B-Chat-Int4](https://www.modelscope.cn/models/qwen/Qwen-7B-Chat-Int4/summary) | 2.3、2.6.2 | llmtuner | ~~llmtuner~~ |  
| [Qwen2-1.5B-Instruct-GPTQ-Int4](https://www.modelscope.cn/models/qwen/Qwen2-1.5B-Instruct-GPTQ-Int4/summary) | 2.5.3 | llmtuner | ~~llmtuner~~ |  
| [Qwen2.5-7B-Instruct-GPTQ-Int4](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4) | 2.7.1 | llmtuner | ~~llmtuner~~ |  
| [RWKV(Seikaijyu微調)](https://huggingface.co/Seikaijyu) | 參見 [HF](https://huggingface.co/Seikaijyu) | rwkv-api | （需要下載配置 RWKV-Runner） |  

本項目的`requirements.txt`基於 `llmtuner` 環境要求搭建，因此我們建議使用 Qwen 系列模型，若選用 ChatGLM 系列模型，可能會導致環境錯誤。  

微調模型下載：[Releases](https://github.com/Moemu/Muice-Chatbot/releases)  

建議將基底模型與微調模型放入 `model` 文件夾中然後在配置文件中配置相應配置項（確保配置文件中的路徑目錄下存在多個模型文件而不是只有一個文件夾，部分微調模型由於疏忽還套了一層 `checkpoint-xxx` 文件夾）  

對於沐雪系列 Qwen 微調模型，建議的配置如下：  

```yaml  
model:  
  loader: llmtuner  
  model_path: model/Qwen2.5-7B-Instruct-GPTQ-Int4 # 基底模型路徑  
  adapter_path: model/Muice-2.7.1-Qwen2.5-7B-Instruct-GPTQ-Int4-8e-4 # 微調模型路徑  
  template: qwen # LLaMA-Factory 中模型的模板（必填）  
  system_prompt: '現在開始你是一個名為的「沐雪」的AI女孩子' # 系統提示（可選）  
  auto_system_prompt: true # 自動配置沐雪的系統提示（默認為 false）  
```  

如果你沒有合適的顯卡，需要通過 CPU 加載模型或者需要加載量化模型，請安裝並配置 `GCC` 環境，然後勾選 `openmp`。[參考連結](https://blog.csdn.net/m0_52985087/article/details/136480206?spm=1001.2014.3001.5501)  

## 脫離沐雪微調模型使用  

本倉庫同時支援脫離沐雪微調模型使用（如直接使用基底模型或使用其他微調模型等），另請參考 [支援的模型加載器列表](./docs/model.md) 配置。  

本倉庫支援調用多模態模型，另請參考 [多模態模型加載器列表](./docs/model.md#多模態模型加載器配置) 。  

## Bot 服務配置  

現以提供 OneBot 服務支援  

本項目使用 [OneBot V11](https://github.com/botuniverse/onebot-11) 協議, 若您希望於 QQ 使用, 推薦參考 [LLOneBot](https://github.com/LLOneBot/LLOneBot) 或  [Lagrange.Core](https://github.com/LagrangeDev/Lagrange.Core)  使用 OneBot 服務  

使用LLOneBot: 請在安裝好 LLOneBot 後, 於設置中開啟反向 WebSocket 服務, 填寫 `ws://127.0.0.1:21050/ws/api`  

使用Lagrange.Core: 請參照 [Lagrange快速部署](https://lagrangedev.github.io/Lagrange.Doc/Lagrange.OneBot/Config/) 完成配置, 並在其配置文件中添加以下配置項  

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

您也可以使用其他 OneBot V11 的適配器連結其他軟體，詳見 [OneBot V11 適配器](https://onebot.dev/ecosystem.html#onebot-%E5%AF%A6%E7%8F%BE-1)  

**能使用請勿隨意更新 QQNT, 若無法使用請嘗試降級 QQNT**  

> [!CAUTION]  
>  
> 2025.02.22 更新：LiteLoaderQQNT導致的封號問題仍未解決。如果仍想繼續使用，可以通過降級到舊版QQNT`9.9.15-2xxxx`，安裝框架後登錄一次並立即關閉，在根目錄下修改文件內容：  
>  
> `\resources\app-update.yml` -> `provider: 3rdparty`  
>  
> `\resources\app\versions\channel.json` -> `"channel": "bbbbbbbbbbeta"`  
>  
> 將修改文件設為唯讀，這樣QQNT將不會自動更新補丁。  

在 Telegram Bot 中使用的方法：[遷移至 Telegram Bot](./docs/telegram.md)  

## 其他功能  

- [語音回覆](docs/other_func.md#語音回覆)  
- [圖像識別（識別 / 發送表情包）](docs/other_func.md#ofa-圖像識別識別--發送表情包)  
- [Faiss 長期記憶](docs/other_func.md#faiss-長期記憶實驗性內容)  
- [實時語音聊天](docs/other_func.md#啟動實時語音聊天)  

# 配置 ⚒️  

配置文件說明位於 `configs.yml`，請根據你的需求進行修改  

# 使用 🎉  

在本項目根目錄下運行 `main.py`  

```powershell  
conda activate Muice  
python main.py  
```  

或是運行自動安裝腳本生成的啟動腳本`start.bat`  

# 命令 🕹️  

| 命令 | 釋義 |  
|------|------|  
| /clean | 清空本輪對話歷史 |  
| /refresh | 刷新本次對話 |  
| /help | 顯示所有可用的命令列表 |  
| /reset | 重置所有對話數據(將存檔對話數據) |  
| /undo | 撤銷上一次對話 |  

# 常見FAQ  

[常見FAQ](./docs/faq.md)  

# 示例對話（訓練集） 📑  

參見公開的訓練集 [Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)  

# 沐雪人設  

與其他聊天機器人項目不同，本項目提供由本人通過自家對話數據集微調後的模型，在 Release 中提供下載，關於微調後的模型人設，目前公開的資訊如下：  

![沐雪人設圖（若無法打開請通過右鍵打開）](https://i0.hdslb.com/bfs/new_dyn/9fc79347b54c5f2835884c8f755bd1ea97020216.png)  

訓練集開源地址： [Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)  

原始模型：[THUDM/ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) & [QwenLM/Qwen](https://github.com/QwenLM/Qwen)）  

本項目源碼使用 [MIT License](https://github.com/Moemu/Muice-Chatbot/blob/main/LICENSE)，對於微調後的模型文件，不建議將其作為商業用途  

# 關於 🎗️  

代碼實現：[Moemu](https://github.com/Moemu)、[MoeSnowyFox](https://github.com/MoeSnowyFox)、[NaivG](https://github.com/NaivG)、[zkhssb](https://github.com/zkhssb)、[Asankilp](https://github.com/Asankilp)  

訓練集編寫與模型微調：[Moemu](https://github.com/Moemu) （RWKV 微調：[Seikaijyu](https://github.com/Seikaijyu)）  

幫助文檔編寫：[TurboHK](https://github.com/TurboHK)、[葉子](https://github.com/FHU-yezi)  

> 友情連接：[Coral 框架](https://github.com/ProjectCoral/Coral)、[nonebot-plugin-marshoai](https://github.com/LiteyukiStudio/nonebot-plugin-marshoai)  

總代碼貢獻：  

<a href="https://github.com/eryajf/Moemu/Muice-Chatbot/contributors">  
  <img src="https://contrib.rocks/image?repo=Moemu/Muice-Chatbot" alt="contributors"/>  
</a>  

如果此項目對你有幫助，您可以考慮贊助。  

<a href="https://www.afdian.com/a/Moemu" target="_blank"><img src="https://pic1.afdiancdn.com/static/img/welcome/button-sponsorme.png" alt="afadian" style="height: 45px !important;width: 163px !important;"></a>  
<a href="https://www.buymeacoffee.com/Moemu" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 45px !important;width: 163px !important;" ></a>  

感謝你們所有人的支持！  

本項目隸屬於 MuikaAI  

官方唯一頻道：[沐雪的小屋](https://pd.qq.com/s/d4n2xp45i)  

Star History：  

[![Star History Chart](https://api.star-history.com/svg?repos=Moemu/Muice-Chatbot&type=Date)](https://star-history.com/#Moemu/Muice-Chatbot&Date)  