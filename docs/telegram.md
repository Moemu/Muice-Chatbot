# 迁移至 Telegram Bot

本篇将介绍 Muice-Chatbot 基于 Telegram Bot 的使用方法

得益于 Onebot V11 协议，我们得以轻松改变代码以便在各个不同的平台中运行。

## 准备你的 Telegram Bot

在 Telegram 中我们可以通过和一个名为 `BotFather` 的机器人交互来申请我们自己的机器人，具体步骤如下

1. 添加 BotFather 为好友：[点击这里](https://telegram.me/botfather) 添加botfather

2. 打开和 Botfather 的对话框发送 `/newbot`

3. 设置机器人的昵称

4. 设置机器人的ID（具有唯一性），结尾必须是`_bot`或者`Bot`

5. 如果上一步执行成功那么botfather会返回该机器人的token，大概长这样

   ```makefile
   123456789:ABCDEfghiJK4314daDSadSa7
   ```

   记住这个 Token，到这里机器人就创建好了

## 修改配置文件

本节说的是 Muice-Chatbot 下的配置文件。

在之前配置好的基础上修改以下内容：

```yaml
platform: telegram # 聊天平台 qq/telegram
```

其他的不用管。

（注：使用 telegram 时会自动覆盖以下配置）

```python
    if configs['bot']['platform'] == 'telegram':
        configs['bot']['cq_code'] = True
        configs['bot']['group']['enable'] = True
        configs['bot']['group']['anyone'] = True
        configs['bot']['group']['only_at'] = False
        configs['bot']['group']['rate'] = 100
```



## 搭建机器人服务

在本篇教程中，我们使用 [Hoshinonyaruko/Gensokyo-Telegram](https://github.com/Hoshinonyaruko/Gensokyo-telegram) 作为服务框架。

进入 [Release](https://github.com/Hoshinonyaruko/Gensokyo-Telegram/releases/tag/4%2Fmerge) 中下载客户端，在控制台中运行此客户端生成配置文件。

在生成的配置文件中修改以下内容：

```yaml
ws_address: ["ws://127.0.0.1:21050/ws/api"] # WebSocket服务的地址 支持多个["","",""]
botToken: "111260888:BBFf5h2cSDoUZctABCD-spo0b2dG4gyEGEG"  # 上一步的Token
httpGetMsg : true  # 使用http轮询获取api
global_group_or_private: true    # 十分建议用群方式获取信息，使用私聊方式存在问题
customcert : true      # 自签名证书，不开没法用
```

重新运行服务，添加你的机器人到**私聊列表**中即可开始使用。

暂不支持群组聊天。