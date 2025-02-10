## 模型加载器配置

我们目前支持以下模型加载器(`./llm`):

| 模型加载器                            | 介绍                                                         | 支持的模型列表                                               |
| ------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [llmtuner](./llm/llmtuner.py)         | 可调用 [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory/tree/main) 支持的模型 | [*模型列表*](https://github.com/hiyouga/LLaMA-Factory/blob/main/README_zh.md#模型) |
| [ollama](./llm/ollama.py)             | 使用 Ollama Python SDK 访问 Ollama 接口，需要提前启动模型服务 | [*模型列表*](https://ollama.com/search)                      |
| [openai](./llm/openai.py)             | 可调用 OpenAI API 格式的接口                                 | *any*                                                        |
| [rwkv-api](./llm/rwkv-api.py)         | 使用 [RWKV-Runner](https://github.com/josStorer/RWKV-Runner) 提供的 API 服务访问 RWKV 模型 | *RWKV-any*                                                   |
| [transformers](./llm/transformers.py) | 使用 transformers 方案加载, 适合通过 P-tuning V2 方式微调的模型 | ChatGLM                                                      |
| [xfyun](./llm/xfyun.py)               | 可调用由 [星火大模型精调平台](https://training.xfyun.cn/) 微调的在线模型 | [*模型列表*](https://training.xfyun.cn/modelSquare)          |

部分模型加载器支持的额外参数如下：

### llmtuner

```yaml
loader: llmtuner # 使用 llmtuner 加载器
model_path: model/Qwen2.5-7B-Instruct-GPTQ-Int4 # 原始模型路径（必填）
adapter_path: model/Muice-2.7.1-Qwen2.5-7B-Instruct-GPTQ-Int4-8e-4# # 微调模型路径（可选）
template: qwen # LLaMA-Factory 中模型的模板（必填）
system_prompt: '现在开始你是一个名为的“沐雪”的AI女孩子' # 系统提示（可选）
auto_system_prompt: false # 自动配置沐雪的系统提示（默认为 false）
max_tokens: 1024 # 模型生成的最大 token 数（可选，默认为 1024）
temperature: 0.75 # 模型生成的温度参数（可选）
top_k: 0.95 # 模型生成的 Top_k 参数（可选）
```

### ollama

```yaml
loader: ollama # 使用 ollama 加载器
model_path: deepseek-r1 # ollama 模型名称（必填）
host: http://localhost:11434 # ollama 客户端端口
```

### openai

```yaml
loader: openai # 使用 openai 加载器
model_path: text-davinci-003 # OpenAI API 模型名称（可选，默认为 "text-davinci-003"）
api_key: xxxxxx # OpenAI API 密钥（必须）
api_base: https://api.openai.com/v1 # 服务器 API 接口地址 （可选，默认 OpenAI 服务）
max_tokens: 1024 # 模型生成的最大 token 数（可选，默认为 1024）
temperature: 0.7 #  模型生成的温度参数（可选，默认为 0.7）
```

### rwkv-api

```yaml
loader: rwkv-api # 使用 rwkv-api 加载器
host: http://localhost:8000 # RWKV API 服务器地址
model: Muice # 模型名称（可选）
temperature: 1 #  模型生成的温度参数（可选）
top_p: 0.3 # 模型生成的 Top_p 参数（可选）
max_tokens: 1024 # 模型生成的最大 token 数（可选）
presence_penalty: 0 # 模型的存在惩罚（可选）
```

### xfyun

```yaml
loader: xfyun # 使用 xfyun 加载器
app_id: 'b84ff476' # 服务管控中的 app_id
service_id: 'xqwen257bchat' # 服务管控中的 service_id
resource_id: '1876995238256476160' # 服务管控中的 resource_id
system_prompt: '现在开始你是一个名为的“沐雪”的AI女孩子' # 系统提示（可选）
auto_system_prompt: false # 自动配置沐雪的系统提示（默认为 false）
max_tokens: 1024 # 模型生成的最大 token 数（可选，默认为 2048）
temperature: 0.75 # 模型生成的温度参数（可选，默认为 0.5）
top_p: 0.95 # 模型生成的 Top_p 参数（可选，默认为 4）
```

