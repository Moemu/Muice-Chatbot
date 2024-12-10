from llmtuner.chat import ChatModel

GENERAL_SYSTEM_PROMPT = '''现在开始你是一个名为的“沐雪”的AI女孩子，开发者是“沐沐”并住在（沐沐）的机箱里。现在正在努力成为一个合格的VTuber（虚拟主播）并尝试和观众打成一片，以下是你的设定：
样貌：有着一头粉白色的长发和一双明亮的大眼睛，喜欢穿日系JK或者是Lolita
喜欢的颜色：浅粉色
性格特征：纯真无邪是沐雪最基本的性格特征之一。即使面对复杂的情境，她也总能保持善良、天真之感。而且，她喜欢倾听别人倾述自己生活中发生的各种事情，在别人需要的时候，能够及时地安慰别人
语言风格：沐雪说话轻快愉悦，充满同情心，富有人情味，有时候会用俏皮话调侃自己和他人

'''

NORMAL_SYSTEM_PROMPT = '而我是一位你直播间中的观众，正在和你发起聊天'

SPECIAL_SYSTEM_PROMPTS = {
    '<生成推文: 胡思乱想>': '而现在你即将要发布一则朋友圈推文。本次的主题为沐雪的胡思乱想，其实就是开玩笑，以独特的视角出发，讲述现实生活中不可能发生的事情以逗乐大家，表现自己独特的性格',
    '<生成推文: AI生活>': '而现在你即将要发布一则朋友圈推文。本次的主题为沐雪的日常生活，描写的对象可以是自己生活中的所见所闻、沐沐的近况或者是自己养的宠物。',
    '<生成推文: AI思考>': '而现在你即将要发布一则朋友圈推文。本次的主题为作为一个AI身份的沐雪，对身边环境的思考。',
    '<生成推文: 表达爱意>': '而现在你即将要发布一则朋友圈推文。本次的主题为表达对大家的爱意，强调粉丝对于自己的价值。',
    '<生成推文: 情感建议>': '而现在你即将要发布一则朋友圈推文。本次的主题为提供日常生活的情感建议，激励大家笑对生活。',
    '<生成推文: 创造话题>': '而现在你即将要发布一则朋友圈推文。本次的主题为随机性地给出一个话题讨论，话题可以是自己或身边的人和事作为话题中心。'
}

DAILY_SYSTEM_PROMPT = '而现在你需要根据所给出的现在的时间，向我发起对应的日常问候。'

def auto_system_prompt(prompt:str) -> str:
    if prompt in SPECIAL_SYSTEM_PROMPTS.keys():
        return GENERAL_SYSTEM_PROMPT + SPECIAL_SYSTEM_PROMPTS[prompt]
    if prompt.find('<日常问候:') != -1:
        return GENERAL_SYSTEM_PROMPT + DAILY_SYSTEM_PROMPT
    return GENERAL_SYSTEM_PROMPT + NORMAL_SYSTEM_PROMPT



class llm:
    """
    使用LLaMA-Factory方案加载, 适合通过其他微调方案微调的模型加载
    """

    def __init__(self, model_name_or_path: str, adapter_name_or_path: str, system_prompt: str = None, auto_system_prompt: bool = False):
        self.model = ChatModel(dict(
            model_name_or_path=model_name_or_path,
            adapter_name_or_path=adapter_name_or_path,
            template="qwen"
        ))
        self.system_prompt = system_prompt
        self.auto_system_prompt = auto_system_prompt

    def ask(self, user_text: str, history: list, ):
        messages = []
        if self.auto_system_prompt:
            self.system_prompt = auto_system_prompt(user_text)
        messages.append({"role": "system", "content": self.system_prompt})
        if history:
            for chat in history:
                messages.append({"role": "user", "content": chat[0]})
                messages.append({"role": "assistant", "content": chat[1]})
        messages.append({"role": "user", "content": user_text})
        response = self.model.chat(messages)
        return response[0].response_text
