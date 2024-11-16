# 配置 Muice

本项目配置文件为 `configs.json`，目前支持配置的项如下：

```json
{
    "model_loader": "transformers",
    "model_name_or_path": "./model/chatglm2-6b",
    "adapter_name_or_path": "./model/Muice",
    "enable_ofa_image": false,
    "ofa_image_model_name_or_path": "",
    "Trust_QQ_list": [],
    "AutoCreateTopic": false,
    "read_memory_from_file": true,
    "known_topic_probability": 0.003,
    "time_topic_probability": 0.75,
    "port":21050,
    "Reply_Wait": true,
    "bot_qq_id":123456789,
    "Is_CQ_Code": false,
    "Group_Message_Reply_Only_To_Trusted": true,
    "Reply_Rate": 50,
    "At_Reply": false,
    "NonReply_Prefix": [],
    "Voice_Reply_Rate": 0
}
```

`model_loader`: 指定模型加载器的类型，当前支持 `api/transformers/llmtuner/rwkv-api`。

`model_name_or_path`: 指定基底模型的名称或路径，例如 `./model/chatglm2-6b`。

`adapter_name_or_path`: 指定预训练模型的名称或路径， 例如 `./model/Muice`。

`enable_ofa_image`: 是否使用 OFA 图像识别。

`ofa_image_model_name_or_path`: OFA 图像识别模型的名称或路径。

`Trust_QQ_list`: 信任 QQ 号列表，只有在此列表中的 QQ 号发送的消息，机器人才会回复。

`AutoCreateTopic`: 是否自动发起新对话。如果启用，将默认以 Trust_QQ_list 中的第一个 QQ 号作为对话发起对象。

`read_memory_from_file`: 是否从文件中读取记忆。这对于项目重启后恢复之前的对话状态非常有用。

`known_topic_probability`: 随机发起已知话题的概率。

`time_topic_probability`: 根据时间（早、中、傍、晚）触发日常问候的概率。

`port`: 反向WebSocket服务的端口号，默认 `21050`。

`Reply_Wait`: （私聊）是否回复时等待一段时间。

`bot_qq_id`: 机器人的 QQ 号。

`Is_CQ_Code`: 是否启用 CQ 码处理信息。

`Group_Message_Reply_Only_To_Trusted`: （群聊）是否仅对信任的 QQ 回复。

`Reply_Rate`: （群聊）机器人回复的概率，取值范围为 0-100。

`At_Reply`: （群聊）是否只回复 @ 机器人的消息。

`NonReply_Prefix`: 消息前缀，机器人不会回复以这些前缀开头的消息。

`Voice_Reply_Rate`: 语音回复的概率，取值范围为 0-100。