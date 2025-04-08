![](src/Cover.png)
<p style="text-align:center">
<img src="https://img.shields.io/github/stars/Moemu/Muice-Chatbot" alt="Stars">
<img src="https://img.shields.io/badge/Model-ChatGLM2--6B & Qwen--7B-green" alt="Model">
<img src="https://img.shields.io/badge/HuggingFace-Dataset-yellow?link=https%3A%2F%2Fhuggingface.co%2Fdatasets%2FMoemu%2FMuice-Dataset" alt="HuggingFace">
<img src="https://img.shields.io/badge/Python-3.10-blue" alt="Python">
<a href='https://pd.qq.com/s/d4n2xp45i'><img src="https://img.shields.io/badge/QQ频道-沐雪的小屋-blue" alt="Stars"></a>
</p>

[简体中文](../Readme.md) | [繁體中文](./Readme_tc.md) | [English](./Readme_en.md) | 日本語

> [!NOTE]
> 私たちは簡体字中国語を使って訓練を行っているので、モデルは日本語からなる質問に答えにくいかもしれません。
> 機械翻訳された日本語訓練集から微調整されたモデルが必要なら、教えてください！

> [!TIP]
> このページの内容は最新ではない可能性があります。私たちはこのページの内容を不定期に更新します。最新の更新を取得するには、簡体字中国語ページから転送してください。

# 紹介 ✨  

Muice（ムイス）は、**自発的**に会話を始めてくれる AI の女の子です。彼女の対話モデルは [Qwen](https://github.com/QwenLM) を微調整したもので、3,000 以上の対話データでトレーニングされています。二次元の女の子らしい話し方で、少しツンデレですが、日常生活の些細なことを楽しんで共有してくれます。毎日違った挨拶をしてくれます。  

# 機能 🪄  

✅ ほぼ完全な自動環境セットアップをサポート  

✅ 3,000 以上の対話データで微調整した Qwen LoRA モデルを提供  

✅ 複数のモデルローダーをサポート（Muice の微調整モデルなしでも使用可能）  

✅ 自発的な会話の開始（ランダムまたは毎日決まった時間に）  

✅ 会話中のリフレッシュなどの操作に 5 つのコマンドを提供  

✅ OFA 画像認識：スタンプの識別、理解、送信  

✅ [fishaudio/fish-speech](https://github.com/fishaudio/fish-speech) を使用した音声合成（Muice TTS モデルはまだ公開されていません）  

✅ グループチャットでの会話（@ で返信またはランダムに返信）  

✅ コンソールでのリアルタイム音声会話（QQ 音声通話はまだサポートされていません）  

✅ 多言語ドキュメント  

✅ よくある質問ガイド  

✅ 明確なログ管理出力  

✅ Faiss メモリモジュール：過去の対話データを検索し、自動的にコンテキストに追加  

# クイックスタート 💻  

推奨環境：  

- Python 3.10  
- 6GB 以上の VRAM を搭載した GPU（int4 量子化の最低要件は 4GB、CPU 推論には 16GB 以上の RAM が必要）  

## 自動インストール（venv）  

現在、すべてのソフトウェアと依存関係の自動インストールが可能です。最新のソースコードを `Code -> Download ZIP` でダウンロードし、解凍してください。  

`install_env.bat` をダブルクリックしてインストールします（**レガシーコンソールを有効にしないでください**）。または、コマンドラインで次のコマンドを実行します：  

```powershell  
.\install_env.bat  
```

自動インストールには時間がかかる場合があります。完了後、モデルを手動でダウンロードする必要があります。  

**自動インストールスクリプトは Python 仮想環境を使用しており、Conda は必要ありません。スクリプトの指示に注意してください。**  

## 手動インストール（Conda を使用）  

```powershell  
git clone https://github.com/Moemu/Muice-Chatbot  
cd Muice-Chatbot  
conda create --name Muice python=3.10.10 -y  
conda activate Muice  
pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple  
```

GPU ユーザーの場合は、さらに以下を実行します：  

```powershell  
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124  
```

GPU ユーザーは、CUDA 環境が設定されていることを確認してください。[参考リンク](https://blog.csdn.net/chen565884393/article/details/127905428)  

## Muice の微調整モデルのロード  

現在サポートされているベースモデルは以下の通りです：  

| ベースモデル | 対応する微調整モデルのバージョン | ローダー | 追加依存ライブラリ |  
|------------|--------------------------------|--------|------------------|  
| [ChatGLM2-6B-Int4](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b-int4/summary) | 2.2-2.4 | transformers | cpm_kernels |  
| [ChatGLM2-6B](https://www.modelscope.cn/models/ZhipuAI/chatglm2-6b/summary) | 2.0-2.3 | transformers | - |  
| [Qwen-7B-Chat-Int4](https://www.modelscope.cn/models/qwen/Qwen-7B-Chat-Int4/summary) | 2.3, 2.6.2 | llmtuner | ~~llmtuner~~ |  
| [Qwen2-1.5B-Instruct-GPTQ-Int4](https://www.modelscope.cn/models/qwen/Qwen2-1.5B-Instruct-GPTQ-Int4/summary) | 2.5.3 | llmtuner | ~~llmtuner~~ |  
| [Qwen2.5-7B-Instruct-GPTQ-Int4](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4) | 2.7.1 | llmtuner | ~~llmtuner~~ |  
| [RWKV (Seikaijyu 微調整)](https://huggingface.co/Seikaijyu) | [HF 参照](https://huggingface.co/Seikaijyu) | rwkv-api | （RWKV-Runner の設定が必要） |  

このプロジェクトの `requirements.txt` は `llmtuner` 環境をベースにしているため、Qwen シリーズのモデルを使用することを推奨します。ChatGLM シリーズのモデルを使用すると、環境エラーが発生する可能性があります。  

微調整モデルのダウンロード：[Releases](https://github.com/Moemu/Muice-Chatbot/releases)  

ベースモデルと微調整モデルを `model` フォルダに配置し、設定ファイルで対応する設定項目を構成してください（設定ファイルのパスがフォルダではなく複数のモデルファイルを指していることを確認してください。一部の微調整モデルは誤って `checkpoint-xxx` フォルダが追加されている場合があります）。  

Muice の Qwen 微調整モデルの推奨設定は以下の通りです：  

```yaml  
model:  
  loader: llmtuner  
  model_path: model/Qwen2.5-7B-Instruct-GPTQ-Int4 # ベースモデルのパス  
  adapter_path: model/Muice-2.7.1-Qwen2.5-7B-Instruct-GPTQ-Int4-8e-4 # 微調整モデルのパス  
  template: qwen # LLaMA-Factory のモデルテンプレート（必須）  
  system_prompt: 'これからあなたは「Muice（ムイス）」という名前のAIの女の子です' # システムプロンプト（オプション）  
  auto_system_prompt: true # Muice のシステムプロンプトを自動構成（デフォルト: false）  
```

適切な GPU がない場合や、CPU でモデルをロードする必要がある場合は、`GCC` 環境をインストールして設定し、`openmp` を有効にしてください。[参考リンク](https://blog.csdn.net/m0_52985087/article/details/136480206?spm=1001.2014.3001.5501)  

## Muice の微調整モデルなしでの使用  

このリポジトリは、Muice の微調整モデルなしで直接ベースモデルや他の微調整モデルを使用することもサポートしています。詳細は [サポートされているモデルローダー](./docs/model.md) を参照してください。  

マルチモーダルモデルの呼び出しもサポートしています。詳細は [マルチモーダルモデルローダー](./docs/model.md#マルチモーダルモデルローダー設定) を参照してください。  

## Bot サービスの設定  

現在、OneBot サービスがサポートされています。  

このプロジェクトは [OneBot V11](https://github.com/botuniverse/onebot-11) プロトコルを使用しています。QQ で使用する場合は、[LLOneBot](https://github.com/LLOneBot/LLOneBot) または [Lagrange.Core](https://github.com/LagrangeDev/Lagrange.Core) を参照してください。  

LLOneBot を使用する場合: インストール後、設定でリバース WebSocket サービスを有効にし、`ws://127.0.0.1:21050/ws/api` を入力してください。  

Lagrange.Core を使用する場合: [Lagrange クイックデプロイ](https://lagrangedev.github.io/Lagrange.Doc/Lagrange.OneBot/Config/) に従って設定し、設定ファイルに以下の設定を追加してください：  

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

他の OneBot V11 アダプターも使用できます。詳細は [OneBot V11 アダプター](https://onebot.dev/ecosystem.html#onebot-%E5%AE%9E%E7%8E%B0-1) を参照してください。  

**必要がない限り QQNT を更新しないでください。問題が発生した場合は、QQNT をダウングレードしてみてください。**  

> [!CAUTION]  
>  
> 2025 年 2 月 22 日更新: LiteLoaderQQNT に関連するアカウント停止問題はまだ解決されていません。引き続き使用したい場合は、QQNT をバージョン `9.9.15-2xxxx` にダウングレードし、フレームワークをインストールして一度ログインした後、すぐに閉じてください。ルートディレクトリで以下のファイルを変更します：  
>  
> `\resources\app-update.yml` -> `provider: 3rdparty`  
>  
> `\resources\app\versions\channel.json` -> `"channel": "bbbbbbbbbbeta"`  
>  
> これらのファイルを読み取り専用に設定すると、QQNT が自動的に更新されなくなります。  

Telegram Bot での使用方法: [Telegram Bot への移行](./docs/telegram.md)  

## その他の機能  

- [音声返信](docs/other_func.md#音声返信)  
- [画像認識（スタンプの識別/送信）](docs/other_func.md#ofa-画像認識スタンプの識別-送信)  
- [Faiss 長期記憶（実験的）](docs/other_func.md#faiss-長期記憶実験的)  
- [リアルタイム音声チャット](docs/other_func.md#リアルタイム音声チャットの開始)  

# 設定 ⚒️  

設定ファイルの説明は `configs.yml` にあります。必要に応じて変更してください。  

# 使用方法 🎉  

プロジェクトのルートディレクトリで `main.py` を実行します：  

```powershell  
conda activate Muice  
python main.py  
```

または、自動インストールスクリプトで生成された `start.bat` を使用します。  

# コマンド 🕹️  

| コマンド | 説明 |  
|---------|-------------|  
| /clean | 現在の対話履歴をクリア |  
| /refresh | 現在の対話をリフレッシュ |  
| /help | 利用可能なすべてのコマンドを表示 |  
| /reset | すべての対話データをリセット（対話データをアーカイブ） |  
| /undo | 最後の対話を元に戻す |  

# よくある質問  

[よくある質問](./docs/faq.md)  

# 対話例（トレーニングデータセット） 📑  

公開データセットを参照: [Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)  

# Muice のキャラクター設定  

他のチャットボットプロジェクトとは異なり、このプロジェクトは独自の対話データセットで微調整されたモデルを提供しており、Releases でダウンロードできます。微調整モデルのキャラクター設定に関する現在公開されている情報は以下の通りです：  

![Muice のキャラクター画像（開けない場合は右クリックで開く）](https://i0.hdslb.com/bfs/new_dyn/9fc79347b54c5f2835884c8f755bd1ea97020216.png)  

トレーニングデータセット: [Moemu/Muice-Dataset](https://huggingface.co/datasets/Moemu/Muice-Dataset)  

ベースモデル: [THUDM/ChatGLM2-6B](https://github.com/THUDM/ChatGLM2-6B) & [QwenLM/Qwen](https://github.com/QwenLM/Qwen)  

このプロジェクトのソースコードは [MIT License](https://github.com/Moemu/Muice-Chatbot/blob/main/LICENSE) を使用しています。微調整されたモデルファイルの商用利用は推奨されません。  

# クレジット 🎗️  

コード実装: [Moemu](https://github.com/Moemu), [MoeSnowyFox](https://github.com/MoeSnowyFox), [NaivG](https://github.com/NaivG), [zkhssb](https://github.com/zkhssb), [Asankilp](https://github.com/Asankilp)  

データセット作成とモデル微調整: [Moemu](https://github.com/Moemu)（RWKV 微調整: [Seikaijyu](https://github.com/Seikaijyu)）  

ドキュメント作成: [TurboHK](https://github.com/TurboHK), [Leaf](https://github.com/FHU-yezi)  

> 関連プロジェクト: [Coral フレームワーク](https://github.com/ProjectCoral/Coral), [nonebot-plugin-marshoai](https://github.com/LiteyukiStudio/nonebot-plugin-marshoai)  

コード貢献:  

<a href="https://github.com/eryajf/Moemu/Muice-Chatbot/contributors">  
  <img src="https://contrib.rocks/image?repo=Moemu/Muice-Chatbot" alt="contributors"/>  
</a>  

このプロジェクトが役に立った場合は、サポートを検討してください。  

<a href="https://www.afdian.com/a/Moemu" target="_blank"><img src="https://pic1.afdiancdn.com/static/img/welcome/button-sponsorme.png" alt="afadian" style="height: 45px !important;width: 163px !important;"></a>  
<a href="https://www.buymeacoffee.com/Moemu" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 45px !important;width: 163px !important;" ></a>  

ご支援いただきありがとうございます！  

このプロジェクトは MuikaAI の一部です。  

公式チャンネル: [Muice の小屋](https://pd.qq.com/s/d4n2xp45i)  

スターの歴史:  

[![Star History Chart](https://api.star-history.com/svg?repos=Moemu/Muice-Chatbot&type=Date)](https://star-history.com/#Moemu/Muice-Chatbot&Date)  