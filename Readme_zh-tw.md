![](src/Cover.png)
<p align="center">
<img src="https://img.shields.io/github/stars/Moemu/Muice-Chatbot" alt="Stars">
<img src="https://img.shields.io/badge/Model-ChatGLM2--6B-green" alt="Model">
<img src="https://img.shields.io/badge/Python-3.10-blue" alt="Python">
</p>

<p align="center">
  <a href="https://github.com/Moemu/Muice-Chatbot/blob/main/Readme.md">簡體中文版</a>
</p>

### 10.20更新：我們已無力提供對qqbot相關程式碼的更新，詳見 https://github.com/Moemu/Muice-Chatbot/issues/18 ，現時我們打算提供一個前端頁面來完成對沐雪的任何互動，對此帶來的不便我深感歉意。

### 由於本作者現在正在高三備戰高考，因此可能無法及時處理任何問題/頻繁提供更新，感謝您的諒解

# 介紹✨

沐雪，一隻會**主動**找你聊天的AI女孩子，其對話模型基於 [ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) 微調而成，訓練集長度1.3K+ *，具有二次元女孩子的說話風格，比較傲嬌，但樂於和你分享生活的瑣碎，每天會給你不一樣的問候。

*：（訓練集長度較低，但我們仍在收集對話數據）

# 功能🪄

✔ 提供本人由 1.5k+ 對話數據微調的 ChatGLM2-6B P-Tuning V2 模型（回答原創率：98%+）

✔ 主動發起聊天（局限於已有的 Prompt）

✔ 提供5條可用的命令

# 使用前須知⚠️
- **本項目不適合零基礎的小白使用!**
- 該項目依賴 pytorch，若不使用支援  [ CUDA （Compute Unified Device Architecture，統一計算架構） ](https://developer.nvidia.com/about-cuda) 的顯卡（NVIDIA 系列顯示卡），處理效率會大幅降低。



# Windows 版本安裝及配置指南🪟

## 1. 最佳系統配置
- 作業系統：Windows 10 及以上/Windows Server 2012 及以上
- 處理器：x86 架構（ARM 可能會出現意料之外的問題）
- 顯示卡：支援 CUDA 運算，**13GB 及以上**顯示記憶體，最低 **5.5GB**（int4）（在日後的更新中，將會針對顯示記憶體需求高的問題進行優化）
- 若使用CPU模式進行推理，需要 **16GB 以上**的記憶體

## 2. 配置運行環境

###  安裝 Python 3.10.10

#### 1. 從 [Python.org](https://www.python.org/downloads/release/python-31010/) 下載適合您系統的安裝包
#### 2. 安裝選項選擇 ```Install for All Users``` 及 ```Add to PATH```
#### 3. 完成安裝

### 安裝 conda
#### 1. 從 [Anacoda.com](https://www.anaconda.com/download/) 下載適合您系統的安裝包
#### 2. 安裝選項選擇 ```Install for All Users``` 及 ```Add to PATH```

### 添加 conda 至系統環境變量中
#### 1. 右鍵點按```本機```（```This PC```）−−>```内容```（```Porperties```）
#### 2. 找到```高級系統設定```（```Advanced System Settings```）−−>```環境變量```（```Environment Variables...``）
#### 3. 在 ```用戶變量```（```User variables for [Your Username]``` ）中 找到 ```Path```一欄，點選```編輯```（```Edit```）−−>```新增```（```New```），新增 Anacoda 路徑。（預設路徑為```C:\ProgramData\anaconda3\Library\bin```、```C:\ProgramData\anaconda3\Scripts```和```C:\ProgramData\anaconda3```，這三者都需要新增到 Path 中）

### 安裝 Pytorch
#### 1. 從 [Pytorch.org](https://pytorch.org/get-started/locally/) 產生並複製適合您設備的命令（請在 ```Package``` 一欄中選擇 ```conda```，在 ```Language``` 一欄中選擇 ```Python```；若您的顯示卡支援 CUDA，請在 ```Compute Platform``` 一欄選擇相應的 CUDA 版本，否則選 ```CPU```）
#### 2. 在您的設備上使用管理員權限啓動 ```命令提示字元```（```cmd```），貼上並執行上一步複製的安裝命令，等待安裝完成


## 3. 安裝及配置項目

### 使用 conda

#### 在 Powershell 中執行下列命令：

```Powershell
git clone https://github.com/Moemu/Muice-Chatbot
cd Muice-Chatbot
conda create --name Muice python=3.10.9
conda activate Muice
pip install -r requirements.txt
```

### 克隆模型

#### 在上一步產生的 `Muice-Chatbot` 資料夾中執行下列命令（**三選一即可！**）

1.原始模型
```
mkdir model
cd model
git lfs install
git clone https://huggingface.co/THUDM/chatglm2-6b
cd ..
```

2.原始模型（int4量化）
```
mkdir model
cd model
git lfs install
git clone https://huggingface.co/THUDM/chatglm2-6b-int4
cd ..
pip install cpm_kernels
```

3.Qwen-7B原始模型（int4量化）
```
mkdir model
cd model
git lfs install
git clone https://huggingface.co/Qwen/Qwen-7B-Chat-Int4
cd ..
pip install peft
pip install optimum
pip install auto-gptq
```

檔案較大，下載需時較久，請耐心等待。

### 下載微調後的模型壓縮檔

從 [Releases](https://github.com/Moemu/Muice-Chatbot/releases) 下載微調後的模型壓縮檔，解壓縮後將其重新命名為 `Muice` 並置於 `model` 資料夾中


### 配置 go-cqhttp
本項目目使用 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 進行機器人交互，请从其 [Releases](https://github.com/Mrs4s/go-cqhttp/releases) 中下載相應的版本及處理程式，並置於 `qqbot` 資料夾中

有關 go-cqhttp 的詳細配置方法及問題，請訪問 [go-cqhttp 主頁](https://docs.go-cqhttp.org/) 及其 [Github 頁面](https://github.com/Mrs4s/go-cqhttp)

### 檔案結構
在最後，您應該得到類似如下所示的檔案結構：
```
Muice-Chatbot    <- 主路徑
 ├─ llm
 ├─ model
 │  ├─ chatglm2-6b         <- 原始模型（三選一）
 │  ├─ chatglm2-6b-int4    <- int4 原始模型（三選一）
 │  ├─ Qwen-7B-Chat-Int4   <- Qwen-7B-int4 原始模型（三選一）
 │  └─ Muice
 ├─qqbot
 │  ├─ go-cqhttp.exe
 │  └─...
 ├─ configs.json  <- Muice 設定檔
 ├─ main.py       <- 主處理程式
 ├─ requirements.txt
 └─...
```

### 配置 Muice
本項目使用 `configs.json` 作為設定檔，目前支援如下功能：

```json
{
    "Trust_QQ_list": [],
    "AutoCreateTopic": false,
    "read_memory_from_file": true,
    "known_topic_probability": "0.003",
    "time_topic_probability": "0.75"
}
```

`Trust_QQ_list`: 信任QQ號列表，只有在列表的QQ號，沐雪才會回覆（留空為全部處理）

`AutoCreateTopic`: 是否自動啟動新對話，預設以 Trust_QQ_list 的第 0 項作為啟動新對話對象

`read_memory_from_file`: 從文件中讀取記憶，用於項目重啟後載入原來的記憶

`known_topic_probability`: 機率：隨機發起一個已知的話題

`time_topic_probability`: 機率：早、中、傍、晚觸發日常問候

## 4. 啓動
在根路徑（```Muice-Chatbot``` 資料夾）中開啓 Powershell，逐行鍵入以下命令：
```powershell
conda activate Muice
python main.py
```

# 命令🕹️

|  命令   | 釋義  |
|  ----  | ----  |
| /clean  | 清空本輪對話歷史 |
| /refresh  | 刷新本次對話 |
| /help  | 顯示所有可用的命令列表 |
| /reset  | 重置所有對話數據(將存檔對話數據) |
| /undo  | 撤銷上一次對話 |

# 示例對話

Q: 你好

> 你好，你今天感覺怎麼樣？

Q: 你知道貓娘嘛

> 唔...不太知道喵...

Q: 雪雪喜歡吃什麼？

>吃·你·而已

Q: 工作又忙又累，還要加班什麼的（此回答不穩定）

> 賺錢嘛，總是伴隨著一些苦逼的活

# 沐雪人設

> ⚠️ 請注意, AI 僅是對人類的自然語言進行模仿，它們是程式和算法的集合，沒有自我意識。如果你在尋找靈魂伴侶，冰冷的算法可能不是個好選擇。

與其他聊天機器人項目不同，本項目提供由本人通過自家對話數據集微調後的模型，在 Release 中提供下載，關於微調後的模型人設，目前公開的信息如下：

> 姓名：沐雪
> 性別：女？
> 年齡：16歲？
> 生日：06.12
> 性格：微傲，喜歡用"本雪"來稱呼自己，但很會關心別人。害怕獨自一個人，不和她聊天的時候她會**主動**找你聊天

# 提報 Issue
> 請注意, 開發者並沒有義務回复您的問題。您應該具備基本的提問技巧。
> 有關如何提問，請閱讀[《提問的智慧》](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way#readme)

原始模型：[THUDM/ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B)

本項目源碼使用 [MIT license](https://github.com/Moemu/Muice-Chatbot/blob/main/LICENSE)，對於微調後的模型文件，不建議作為商業用途

# 關於🎗️

代碼編寫：[Moemu](https://github.com/Moemu)

安裝及配置指南編寫：[TurboHK](https://github.com/TurboHK)

模型訓練：[Moemu](https://github.com/Moemu)

訓練集編寫：[Moemu](https://github.com/Moemu)

文檔繁體中文化：[TurboHK](https://github.com/TurboHK)

代碼貢獻：

<a href="https://github.com/eryajf/Moemu/Muice-Chatbot/contributors">
  <img src="https://contrib.rocks/image?repo=Moemu/Muice-Chatbot" />
</a>

Star History：

[![Star History Chart](https://api.star-history.com/svg?repos=Moemu/Muice-Chatbot&type=Date)](https://star-history.com/#Moemu/Muice-Chatbot&Date)
