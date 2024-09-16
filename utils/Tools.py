import re
import random

def divide_sentences(text: str) -> list:
    """
    切分一段句子
    """
    sentences = re.findall(r'.*?[~。！？…]+', text)
    if len(sentences) == 0:
        return [text]
    if len(''.join(sentences)) < len(text):
        sentences.append(text.lstrip(''.join(sentences))) # 避免当句子后面没句号时被忽略的情况
    return sentences

def process_at_message(is_cq_code: bool, data) -> tuple[bool, list, str]:
    """
    处理消息中的 @ 提及信息。
    Args:
    - is_cq_code (bool): 是否是 CQ 码。
    - message (Any): 输入的消息数据。
    Returns:
    - tuple: 包含三个元素：
        - is_at_message (bool): 是否是 @ 提及消息。
        - at_matches (list): 有匹配的 @ 提及集合。
        - processed_message (str): 处理后的消息字符串。
    """
    if is_cq_code:
        if isinstance(data, dict):
            message = data['message']
        else:
            message = data
        at_pattern = re.compile(r'\[CQ:at,qq=(\d+)(?:,name=\w+)?\]')
        at_matches = at_pattern.findall(message)
        if at_matches:
            processed_message = at_pattern.sub(lambda m: '', message)
            return True, at_matches, processed_message
        else:
            return False,at_matches, message
    else:
        at_qq_list = []
        message = ' '.join([item['data']['text'] for item in data['message'] if item['type'] == 'text'])
        for msg in data.get('message', []):
            if msg.get('type') == 'at':
                at_qq_list.append(msg['data']['qq'])
        if at_qq_list and len(at_qq_list) > 0:
            return True, at_qq_list, message
        return False, at_qq_list, message
    
def is_reply_message(at_reply: bool, reply_rate: int, is_at_message: bool) -> bool:
    """
    判断是否是回复消息。
    Args:
    - at_reply (bool): 是否是 @ 回复。
    - reply_rate (int): 回复率。
    - is_at_message (bool): 是否是 @ 提及消息。
    Returns:
    - bool: 是否是回复消息。
    """
    if at_reply:
        return True
    elif is_at_message:
        return True
    elif random.randint(1, 100) <= reply_rate:
        return True
    else:
        return False
    
def is_image_message(is_cq_code: bool, data) -> tuple[bool, str]:
    """
    判断是否是图片消息。
    Args:
    - is_cq_code (bool): 是否是 CQ 码。
    - data (Any): 消息数据。
    Returns:
    - tuple: 包含两个元素：
        - is_image (bool): 是否是图片消息。
        - image_url (str): 图片 URL。
    """
    if is_cq_code:
        if isinstance(data, dict):
            message = data['message']
        else:
            message = data
        url_pattern = r"url=(https?[^,]+)"
        image_match = re.search(url_pattern, message)
        if image_match:
            image_url = image_match.group(1)
            return True, image_url
        url_pattern = r"url=(file[^,]+)"
        image_match = re.search(url_pattern, message)
        if image_match:
            image_url = image_match.group(1)
            return True, image_url
        else:
            return False, ''
    else:
        for msg in data.get('message', []):
            if msg.get('type') == 'image':
                image_url = msg['data'].get('url')
                return True, image_url
        return False, ''
    
def voice_message_reply(voice_rate: str) -> bool:
    """
    判断是否回复语音消息。
    Args:
    - voice_rate (str): 语音回复率。
    Returns:
    - bool: 是否回复语音消息。
    """
    if random.randint(1, 100) <= int(voice_rate):
        return True
    else:
        return False

