import re

def process_thoughts(message:str, output_thoughts:int = 1) -> list[str|None, str]:
    """
    思维链处理
    """
    thoughts_pattern = re.compile(r'<think>(.*?)</think>', re.DOTALL)
    thoughts_match = thoughts_pattern.search(message)
    thoughts = thoughts_match.group(1) if thoughts_match else ""
    if thoughts == "\n\n":
        thoughts = "无"
    else:
        thoughts = thoughts.replace('\n','')
    respond = thoughts_pattern.sub('', message).strip()
    if output_thoughts == 2:
        return [None, respond]
    else:
        return ['思考过程：' + thoughts, respond]