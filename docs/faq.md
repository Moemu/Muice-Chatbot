# 常见FAQ指南

## 通用解决方案

先把报错内容自己读一遍，上面写什么你就尝试着自己修复，如果看不懂就上网搜，实在不行再提问。

如果你使用 Conda，在执行下面的指令前请先激活环境。

```powershell
conda activate Muice
```

如果你使用自动脚本中的虚拟环境，也请激活环境：

```powershell
call Muice\Scripts\activate.bat
```

## AssertionError: Torch not compiled with CUDA enabled

排查方案：

1. 检查 `pytorch.cuda.is_available`：

   ```powershell
   Python 3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)] on win32
   Type "help", "copyright", "credits" or "license" for more information.
   >>> import torch
   >>> print(torch.cuda.is_available())
   True <-- 是否为 True
   ```

   如果为 False ，请执行：

   ```powershell
   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
   ```

   然后进行第二步，否则继续。

   

2. 检查 Pytorch 版本：

   ```powershell
   pip list
   ```

   ```powershell
   Package            Version
   ------------------ ------------
   certifi            2023.7.22
   ...
   torch              2.0.1+cu118 <-- 检查是否为cuda版本
   torchaudio         2.0.2+cu118
   torchvision        0.15.2+cu118
   ...
   
   [notice] A new release of pip is available: 23.0.1 -> 23.2.1
   [notice] To update, run: python.exe -m pip install --upgrade pip
   ```

   如果不是，请执行第一步。

3. 检查 `nvcc` 安装：

   ```bash
   nvcc --version
   ```

   如果失败，请参考：https://www.cnblogs.com/zijie1024/articles/18375637

   如果你使用 Conda 环境，则可以参考：https://zhuanlan.zhihu.com/p/367740437

参考Issue：https://github.com/Moemu/Muice-Chatbot/issues/2

## cuda extension not installed

`auto_gptq` 需要自行编译，直接从 pip 拉取的版本将会导致模型推理速度下降。

在这之前，请检查 `nvcc` 安装并配置 `CUDA_HOME` 环境变量（比如 `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6`）

```powershell
git clone https://github.com/PanQiWei/AutoGPTQ.git && cd AutoGPTQ
pip install -vvv --no-build-isolation -e .
```

## git : 无法将“git”项识别为 cmdlet...请确保路径正确

未安装Git，参考：https://blog.csdn.net/mukes/article/details/115693833

## 从HuggingFace拉取模型时较慢

请使用镜像站：https://hf-mirror.com/

对于国内大模型，还可以使用：https://www.modelscope.cn/

## FileNotFoundError: Could not find module 'C:\Users\\...\chatglm2-6b-int4\quantization_kernels_parallel.so' (or one of its dependencies). Try using the full path with constructor syntax.

根据报错输出，在配置文件中把模型路径改成绝对路径

```yaml
  model_path: D:\Muice-Development\model\Qwen2.5-7B-Instruct-GPTQ-Int4 # 基底模型路径
  adapter_path: D:\Muice-Development\model\Muice-2.7.1-Qwen2.5-7B-Instruct-GPTQ-Int4-8e-4 # 微调模型路径
```

## error: Microsoft Visual C++ 14.0 or greater is required.

前往 https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/ 获取C++生成工具，安装后勾选使用C++的桌面开发，下载安装即可

## ModuleNotFoundError: No module named "..."

下载对应的第三方库即可

```powershell
pip instal ...
```

## ImportError: This modeling file requires the following packages that were not found in your environment:'tiktoken'. Run 'pip install tiktoken'

不会读英文的可以把整个 Chatbot 文件夹删除了，我们的项目不适合您。

```powershell
pip install tiktoken
```

## OSError: Incorrect path_or_ model_id: './model/chatglm2-6b'. please provide either the path to a local folder or the repo id of a model on the Hub.

路径不对，找不到文件，修改配置文件中模型的位置，确保它真实存在，实在不行就写绝对路径就行了。

```yaml
  model_path: D:\Muice-Development\model\Qwen2.5-7B-Instruct-GPTQ-Int4 # 基底模型路径
  adapter_path: D:\Muice-Development\model\Muice-2.7.1-Qwen2.5-7B-Instruct-GPTQ-Int4-8e-4 # 微调模型路径
```

