import re
from typing import List

def divede_sentences(text: str) -> List[str]:
    '''
    切分一段句子
    '''
    sentences = re.findall(r'.*?[~。！？…]+', text)
    if len(sentences) == 0:
        return [text]
    return sentences
