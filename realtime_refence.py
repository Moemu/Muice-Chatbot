import pyaudio
import numpy as np
import wave
import logging
import os
import importlib
import json
import asyncio
from pydub import AudioSegment
from pydub.playback import play
import sounddevice as sd

from Muice import Muice
from utils.fish_speech_api import fish_speech_api
from utils.audio_process import SpeechRecognitionPipeline
import threading

CHUNK = 1024  # 每次读取的音频块大小
FORMAT = pyaudio.paFloat32  # 音频格式
CHANNELS = 1  # 声道
RATE = 22050  # 采样率
THRESHOLD = 75  # 声音响度阈值
SILENCE_THRESHOLD_MS = 1500  # 静音持续时间阈值（毫秒）
SILENCE_COUNT = int(SILENCE_THRESHOLD_MS / (1000 * CHUNK / RATE))  # 静音计数器阈值
use_virtual_device = False  # 是否使用虚拟设备
if use_virtual_device:
    speaker_device_index = 3  # 输入设备索引
    mic_device_index = 10  # 输出设备索引
    device_index = speaker_device_index
else:
    device_index = 1  # 录音设备索引

p = pyaudio.PyAudio()

def play_audio(file_path):
    if not use_virtual_device:
        sound = AudioSegment.from_file(file_path)
        play(sound)
    else:
        audio = AudioSegment.from_wav(file_path)
        audio_array = np.array(audio.get_array_of_samples())
        sample_rate = audio.frame_rate
        channels = audio.channels
        if channels == 2:
            audio_array = audio_array.reshape((-1, 2)).mean(axis=1)
        audio_data = audio_array / np.iinfo(audio_array.dtype).max
        sd.play(audio_data, sample_rate, device=mic_device_index)
        sd.wait()




stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=device_index)

def save_wav(frames, filename):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

# 读取配置文件
configs = json.load(open('configs.json', 'r', encoding='utf-8'))
model_loader = configs["model_loader"]
model_name_or_path = configs["model_name_or_path"]
adapter_name_or_path = configs["adapter_name_or_path"]
audio_name_or_path = configs["audio_name_or_path"]

# 加载模型
SpeechRecognitionPipeline.load_model(audio_name_or_path)
model = importlib.import_module(f"llm.{model_loader}")
model = model.llm(model_name_or_path, adapter_name_or_path)

muice_app = Muice(model, configs['read_memory_from_file'], configs['known_topic_probability'],
                  configs['time_topic_probability'])


# 检查并创建临时文件夹
if not os.path.exists('./audio_tmp'):
    os.makedirs('./audio_tmp')

# 开始录音
logging.info("开始录音...")

async def record_audio():
    try:
        while True:
            frames = []
            silence_count = 0

            while True:
                data = np.frombuffer(stream.read(CHUNK), dtype=np.float32)  # 明确指定数据类型
                if np.any(data < -32768) or np.any(data > 32767) or np.any(np.isnan(data)):
                    logging.warning("音频数据有误，忽略此次录音")
                    rms = 0  # 声音响度为0
                else:
                    squared_data = np.square(data)
                    rms = np.sqrt(np.mean(squared_data)) * 1000  # 计算RMS
                        
                if np.isnan(rms) or np.isinf(rms):
                    rms = 0  # 如果是非法值，将其设为0

                if rms * 2 > THRESHOLD:
                    print(f"当前音量: {rms}")
                if rms > THRESHOLD:
                    silence_count = 0
                    frames.append(data.tobytes())
                else:
                    silence_count += 1
                    if silence_count > SILENCE_COUNT:
                        break

            if frames:
                output_filename = f"./audio_tmp/output_{len(frames)}.wav"
                save_wav(frames, output_filename)
                logging.info(f"已保存音频文件: {output_filename}，开始语音处理")
                message = await SpeechRecognitionPipeline().generate_speech(output_filename)
                # 语音处理完毕后，删除临时文件
                os.remove(output_filename)
                reply = muice_app.ask(text=message, user_qq="realtime_refence", group_id=-1)
                logging.info(f"回复消息：{reply}")
                muice_app.finish_ask(reply)
                try:
                    voice_file = await fish_speech_api(reply)
                    voice_file = os.path.abspath(voice_file)
                    voice_file = os.path.normpath(voice_file)
                    logging.info(f"尝试播放的音频文件路径: {voice_file}")
                    if voice_file:
                        t = threading.Thread(target=play_audio, args=(voice_file,))
                        t.start()
                        t.join()
                        os.remove(voice_file)
                    else:
                        logging.info("没有找到合适的语音文件")
                except Exception as e:
                    logging.error(f"播放语音文件失败: {e}")

    except KeyboardInterrupt:
        pass

    print("录音结束.")

    stream.stop_stream()
    stream.close()
    p.terminate()

async def main():
    await record_audio()

asyncio.run(main())
