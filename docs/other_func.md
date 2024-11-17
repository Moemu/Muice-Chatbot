# 其他功能

Muice 还支持一些其他功能，如 [Faiss 长期记忆](#faiss-长期记忆实验性内容)、[OFA 图像识别](#ofa-图像识别识别--发送表情包)、[语音回复](#语音回复)、[启动实时语音聊天](#启动实时语音聊天) 。

## Faiss 长期记忆（实验性内容）

本项目支持 Faiss 向量记忆，即将聊天记录保存至 Faiss 中，以便长期记忆。

若您希望使用 Faiss 向量记忆，请在配置文件中设置 `enable_faiss` 为 `true`，并设置 `sentence_transformer_model_name_or_path` 为 `sentence-transformers` 模型的路径。

Faiss 记忆用到的 `sentence-transformers` 模型需要额外下载（理论上所有 `sentence-transformers` 模型都可以）：

| 推荐 `sentence-transformers` 模型                                                      |
| ------------------------------------------------------------ |
| [distiluse-base-multilingual-cased-v1](https://hf-mirror.com/sentence-transformers/distiluse-base-multilingual-cased-v1)|

Faiss 向量库位于 `memory` 文件夹中，一共三个文件：`faiss_index.faiss`、`faiss_index.faiss.docstore`、`faiss_index.faiss.mapping`，三者一一对应，改动前请注意备份。

### 导入 CSV 记忆

下载 CSV 记忆文件，确保其内部格式（**UTF-8**）为：

```csv
topic1\tcontent1
topic2\tontent2
...
```

将文件放入根目录，运行导入程序：

```powershell
python import_csv_memory.py
```

输入文件名（**包括 `.csv` 后缀**），程序将自动导入 Faiss 向量库中。

## OFA 图像识别（识别 / 发送表情包）

本项目支持 OFA 图像识别，即对聊天图片进行特征提取，并通过 OFA 模型进行描述生成。发送信息时，会检索本地图片库，若存在匹配的图片，则会发送图片。

若您希望使用OFA图像识别，请在配置文件中设置 `enable_ofa_image` 为 `true`，并设置 `ofa_image_model_name_or_path` 为 OFA 图像识别模型的路径。

OFA 使用到的依赖需要额外安装：

```powershell
conda activate Muice
pip install -r ofa_requirements.txt
```

目前支持的 OFA 模型如下表：

| OFA 模型                                                      |
| ------------------------------------------------------------ |
| [OFA-Image-Caption-Meme-Large-ZH](https://www.modelscope.cn/models/iic/ofa_image-caption_meme_large_zh) （建议） |
| [ofa_image-caption_muge_base_zh](https://www.modelscope.cn/models/iic/ofa_image-caption_muge_base_zh) |

本地图片数据库位于 `image_data` 文件夹中，程序会每五分钟备份一次数据库，默认保留5个备份槽位。

若您想要回退数据库到某个时间点，请将 `image_data` 文件夹中的 `image_data.db` 删除，并将备份槽位文件 `image_data.db.backup_xxx_xxx` 修改为 `image_data.db`。

## 语音回复

若您希望使用语音回复，请在配置文件中设置 `Voice_Reply_Rate` 为大于 0 的整数，机器人将会以设置的概率回复语音消息。

语音回复使用到的项目：[fishaudio/fish-speech](https://github.com/fishaudio/fish-speech)

在 fish-speech 的 WebUI 启动（使用 `--infer` 参数）后，更改 `fish_speech_api.py` 中的 `Client`、`reference_audio`、`reference_text` 即可。

- `Client` 为 fish-speech 的 WebUI 地址

- `reference_audio` 为参考音频文件路径，此音频用于变声效果。

- `reference_text` 为参考音频文件的参考文本。

## 启动实时语音聊天

1.安装依赖：

```powershell
conda activate Muice
pip install -r audio_requirements.txt
```

2.安装配置语音回复（详见上文）

3.获取语音识别模型

目前支持的模型如下表：

| 语音识别模型                                                                                                                  |
|---------------------------------------------------------------------------------------------------------------------------------|
| [SenseVoice 多语言语音理解模型 Small](https://www.modelscope.cn/models/iic/SenseVoiceSmall) |

你可以通过以下命令下载并解压模型：

```powershell
modelscope download --model iic/SenseVoiceSmall --local_path ./SenseVoice
```

下载完成后，在配置文件中设置 `audio_name_or_path` 为模型文件夹的路径。

4.配置信息和设备

你可以通过以下命令查看输入输出设备信息：

```powershell
python realtime_refence.py --get_device
```
在 `realtime_refence.py` 中配置输入输出设备信息：

```python

CHUNK = 1024  # 每次读取的音频块大小
FORMAT = pyaudio.paFloat32  # 音频格式
CHANNELS = 1  # 输入设备声道
RATE = 22050  # 采样率（16000/22050/44100）
THRESHOLD = 75  # 声音响度阈值（60-150左右，请根据实际情况调节）
SILENCE_THRESHOLD_MS = 1500  # 静音持续时间阈值（毫秒）
SILENCE_COUNT = int(SILENCE_THRESHOLD_MS / (1000 * CHUNK / RATE))  # 静音计数器阈值
use_virtual_device = False  # 是否使用虚拟设备（当你需要通过语音通话时，请设置为True）
if use_virtual_device:
    speaker_device_index = 3  # 虚拟输入设备索引
    mic_device_index = 10  # 虚拟输出设备索引
    device_index = speaker_device_index
else:
    device_index = 1  # 录音设备索引

```

4.启动实时语音聊天

```powershell
python realtime_refence.py
```