import pyaudio
import sounddevice as sd
p = pyaudio.PyAudio()

# 获取设备总数
device_count = p.get_device_count()

# 打印所有设备的信息
for i in range(device_count):
    device_info = p.get_device_info_by_index(i)
    print(f"Device {i}: {device_info['name']}")

p.terminate()
