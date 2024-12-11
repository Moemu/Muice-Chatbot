![](../src/Cover.png)
<p style="text-align:center">
<img src="https://img.shields.io/github/stars/Moemu/Muice-Chatbot" alt="Stars">
<img src="https://img.shields.io/badge/Model-ChatGLM2--6B & Qwen--7B-green" alt="Model">
<img src="https://img.shields.io/badge/HuggingFace-Dataset-yellow?link=https%3A%2F%2Fhuggingface.co%2Fdatasets%2FMoemu%2FMuice-Dataset" alt="HuggingFace">
<img src="https://img.shields.io/badge/Python-3.10-blue" alt="Python">
</p>

[简体中文](../Readme.md) | [繁體中文](./Readme_tc.md) | [English](./Readme_en.md) | 日本語

> [!IMPORTANT]
> 2024.12.04更新：プロファイルフォーマットの変更により、本Repoを引き出し、12.04後にfetch操作を実行したことがある場合は、プロファイルを再設定してください。ご不便をおかけして申し訳ありません。

> [!WARNING]
> 私たちは簡体字中国語を使って訓練を行っているので、モデルは日本語からなる質問に答えにくいかもしれません。
機械翻訳された日本語訓練集から微調整されたモデルが必要なら、教えてください！

> [!TIP]
> このページの内容は最新ではない可能性があります。私たちはこのページの内容を不定期に更新します。最新の更新を取得するには、簡体字中国語ページから転送してください。

# イントロダクション✨

**Muice** は、話しかけてくるAI女の子「沐雪（ムユ）」です。その対話モデルは [ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) および [Qwen](https://github.com/QwenLM) を微調整したもので、3,000以上のデータセットを使用してトレーニングされています。特徴としては、二次元の女の子のような話し方で、少しツンデレですが、日々の些細なことを喜んで共有し、毎日異なる挨拶をしてくれます。

------

# 機能🪄

✅ ほぼ全自動で環境をインストール可能

✅ ChatGLM2-6B P-Tuning V2モデルとQwen Qlora微調整モデルを提供

✅ ランダム、または毎日朝・昼・夕方・夜の固定時間に会話を開始

✅ チャット中にリフレッシュや返信操作を行うための5つのコマンドを提供

✅ OFA画像認識：スタンプや画像の識別、理解、送信

✅ [fishaudio/fish-speech](https://github.com/fishaudio/fish-speech) を使った音声合成に対応（沐雪TTSモデルは未公開）

✅ グループチャットでの会話（@での返信やランダム返信に対応）

✅ コンソールでリアルタイムに対話可能（QQ音声通話には未対応）

✅ 多言語ドキュメントを提供

⬜ 記憶モジュールを最適化し、長期記憶と短期記憶を実現

⬜ ログ記録メカニズムを改善し、自動でバグ報告を生成

⬜ よくある質問（Q&A）のガイドを作成

以下是文档的第二部分翻译：

------

# クイックスタート💻

**推奨環境：**

- Python 3.10+
- 6GB以上のビデオメモリを持つGPU（int4量子化では最低4GB、CPU推論には16GB以上のメモリが必要）

## 自動インストール

現在、すべてのソフトウェアと依存関係を自動的にインストール可能です。`Code -> Download ZIP` で最新のソースコードをダウンロード・解凍してください。

インストールには、`install_env.bat` をダブルクリックするか、以下のコマンドをコマンドラインで実行します：

```powershell
.\install_env.bat
```

自動インストールには時間がかかる場合があります。完了後、モデルを手動でダウンロードする必要があります。

**注意：自動インストールスクリプトはPython仮想環境を使用しており、Condaは必要ありません。インストールスクリプトの指示に従ってください。**

## 手動インストール（Conda使用時）

以下の手順で手動インストールを行います：

```powershell
git clone https://github.com/Moemu/Muice-Chatbot
cd Muice-Chatbot
conda create --name Muice python=3.10.10 -y
conda activate Muice
pip install -r requirements.txt
```

GPUを使用する場合は、さらに以下を実行してください：

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

また、CUDA環境が正しく設定されていることを確認してください。[参考リンク(ZH)](https://blog.csdn.net/chen565884393/article/details/127905428)

## モデルのダウンロードとロード

現在、以下の基盤モデルがサポートされています：

| **基盤モデル**                                               | **対応する微調整モデルのバージョン**                 | **追加依存ライブラリ**       |
| ------------------------------------------------------------ | ---------------------------------------------------- | ---------------------------- |
| [ChatGLM2-6B-Int4](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b-int4/summary) | 2.2-2.4                                              | cpm_kernels                  |
| [ChatGLM2-6B](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b/summary) | 2.0-2.3                                              |                              |
| [Qwen-7B-Chat-Int4](https://www.modelscope.cn/models/qwen/Qwen-7B-Chat-Int4/summary) | 2.3、2.6.2                                           | llmtuner                     |
| [Qwen2-1.5B-Instruct-GPTQ-Int4](https://www.modelscope.cn/models/qwen/Qwen2-1.5B-Instruct-GPTQ-Int4/summary) | 2.5.3                                                | llmtuner                     |
| [Qwen2.5-7B-Instruct-GPTQ-Int4](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4) | 2.7.1                                                | llmtuner                     |
| [RWKV(Seikaijyu 微調整)](https://huggingface.co/Seikaijyu)   | 詳細は [HF](https://huggingface.co/Seikaijyu) を参照 | （RWKV-Runner の設定が必要） |

微調整済みモデルのダウンロード：[Releases](https://github.com/Moemu/Muice-Chatbot/releases)

基盤モデルおよび微調整モデルを`model`フォルダに配置してください（微調整モデルフォルダの中に`.model`ファイルが直接存在する必要があります。一部の微調整モデルは誤ってさらに`checkpoint`フォルダが追加されている場合があります）。

## サポートされるモデルのロード方式

本リポジトリでは以下の方法でモデルをロードできます：

1. APIを介してロード
2. `transformers` の `AutoTokenizer` および `AutoModel` 関数を使用
3. `llmtuner.chat`（`LLaMA-Factory`）の `ChatModel` クラスを使用
4. `RWKV-Runner` が提供するAPIサービスを使用

テスト済みモデルの中で、以下のロード方法を推奨します：

| **基盤モデル**           | **微調整方式** | **ロード方法** |
| ------------------------ | -------------- | -------------- |
| ChatGLM                  | P-tuning V2    | transformers   |
| Qwen                     | sft            | llmtuner       |
| RWKV（Seikaijyu 微調整） | pissa          | rwkv-api       |

## Botサービス設定

現在、OneBotサービスがサポートされています。これにより、gocqの制限を回避できます。

本プロジェクトは [OneBot V11](https://github.com/botuniverse/onebot-11) プロトコルを使用しています。QQで使用する場合は、[LLOneBot](https://github.com/LLOneBot/LLOneBot) を参考にOneBotサービスを利用することをお勧めします。

**注意**: LLOneBotをインストールした後、設定で逆WebSocketサービスを有効にし、`ws://127.0.0.1:21050/ws/api` を入力してください。これにより正常に動作します。

また、[Lagrange.Core](https://github.com/LagrangeDev/Lagrange.Core) や [~~OpenShamrock~~](https://github.com/whitechi73/OpenShamrock) などを使用してQQに接続することもできます。他のソフトウェアと接続する場合は、[OneBot V11適配器](https://onebot.dev/ecosystem.html#onebot-实现-1) を参照してください。

**QQNTの不要なアップデートは避けてください。使用できない場合は、QQNTをダウングレードして試してください。**


## その他の機能（中国語ドキュメント）

- [音声応答](https://chatgpt.com/c/docs/other_func.md#音声応答)
- [画像認識（スタンプの識別・送信）](https://chatgpt.com/c/docs/other_func.md#ofa-画像認識識別--送信)
- [Faissによる長期記憶](https://chatgpt.com/c/docs/other_func.md#faiss-長期記憶実験的内容)
- [リアルタイム音声チャット](https://chatgpt.com/c/docs/other_func.md#リアルタイム音声チャットの開始)

## まとめ

すべての設定を完了すると、以下のようなファイル構成になるはずです：

```
Muice-Chatbot     <- 主ディレクトリ  
 ├─llm  
 ├─model  
 │  ├─ chatglm2-6b       <- オリジナルモデル（以下の3つから1つを選択）  
 │  ├─ chatglm2-6b-int4  <- int4オリジナルモデル  
 │  ├─ Qwen-7B-Chat-Int4 <- Qwen-7B-int4オリジナルモデル  
 │  └─ Muice             <- 微調整済みモデル  
 ├─configs.yml  <- 設定ファイル  
 ├─ws.py        <- wsサービス  
 ├─main.py      <- メインスクリプト  
 ├─requirements.txt  
 └─...  
```

------

# 設定⚒️

設定ファイルは `configs.yml` にあり、必要に応じて編集してください。

**2024年12月4日の更新内容**：
 設定ファイルのフォーマットが変更されました。2.7.x以降のモデルに対応するため、以下の項目が追加されました：

```yaml
# アクティブな対話に関する設定  
active:  
  enable: false # アクティブな対話を有効にするか  
  rate: 0.003   # アクティブな対話の確率（毎分）  
  active_prompts:  
    - '<生成推文: 胡思乱想>'
    - '<生成推文: AI生活>'
    - '<生成推文: AI思考>'
    - '<生成推文: 表达爱意>'
    - '<生成推文: 情感建议>'
  not_disturb: true # おやすみモードを有効にするか  
  schedule:  
    enable: true # スケジュールタスクを有効にするか  
    rate: 0.75   # スケジュールタスクの確率（毎回）  
    tasks:  
      - hour: 8
        prompt: '<日常问候: 早上>'
      - hour: 12
        prompt: '<日常问候: 中午>'
      - hour: 18
        prompt: '<日常问候: 傍晚>'
      - hour: 22
        prompt: '<日常问候: 深夜>'  
  targets: # アクティブな対話の対象となるQQ番号  
    - 12345678  
    - 23456789  
```

**2.7.x以前のモデルを使用している場合**、以下のように変更してください：

```yaml
  active_prompts:
    - '（分享一下你的一些想法）'
    - '（创造一个新话题）'
```

また、以下の部分も変更してください：

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

以下是文档的日语翻译：

# 使用🎉

プロジェクトのルートディレクトリで `main.py` を実行します：

```powershell
conda activate Muice
python main.py
```

または、自動インストールスクリプトによって生成された起動スクリプト `start.bat` を実行します。

# コマンド🕹️

| コマンド | 意味                                                 |
| -------- | ---------------------------------------------------- |
| /clean   | 現在の会話履歴を削除する                             |
| /refresh | この会話をリフレッシュする                           |
| /help    | 利用可能なすべてのコマンドリストを表示する           |
| /reset   | すべての会話データをリセットする（会話データを保存） |
| /undo    | 最後の会話を元に戻す                                 |

# サンプル会話（トレーニングセット）📑

公開されているトレーニングセット [Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset) を参照してください。

# 沐雪キャラクター設定

他のチャットボットプロジェクトとは異なり、本プロジェクトでは、独自の会話データセットを基に微調整されたモデルを提供しており、リリースからダウンロードできます。微調整後のモデルのキャラクター設定について、現在公開されている情報は以下の通りです：

![沐雪キャラクター画像（開けない場合は右クリックして開いてください）](https://i0.hdslb.com/bfs/new_dyn/9fc79347b54c5f2835884c8f755bd1ea97020216.png)

トレーニングセットオープンソースリンク：[Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)

元のモデル：[THUDM/ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) と [QwenLM/Qwen](https://github.com/QwenLM/Qwen)

本プロジェクトのソースコードは [MIT License](https://github.com/Moemu/Muice-Chatbot/blob/main/LICENSE) のもとで公開されており、微調整後のモデルファイルは商業目的での使用を推奨しません。

# お知らせ🎗️

**コード実装：**[Moemu](https://github.com/Moemu)、[MoeSnowyFox](https://github.com/MoeSnowyFox)、[NaivG](https://github.com/NaivG)、[zkhssb](https://github.com/zkhssb)

**トレーニングセット作成とモデル微調整：**[Moemu](https://github.com/Moemu)（RWKV微調：[Seikaijyu](https://github.com/Seikaijyu)）

**ヘルプ文書作成：**[TurboHK](https://github.com/TurboHK)、[叶子](https://github.com/FHU-yezi)

> **友好リンク：**[Coralフレームワーク](https://github.com/ProjectCoral/Coral)

総コード貢献：

<a href="https://github.com/eryajf/Moemu/Muice-Chatbot/contributors">
  <img src="https://contrib.rocks/image?repo=Moemu/Muice-Chatbot"  alt="Loading..."/></a>

このプロジェクトが役立った場合は、サポートをご検討ください：

<a href="https://www.buymeacoffee.com/Moemu" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 45px !important;width: 163px !important;" ></a>

ご支援いただきありがとうございます！

**Star History：**

![Star History Chart](https://api.star-history.com/svg?repos=Moemu/Muice-Chatbot&type=Date)
