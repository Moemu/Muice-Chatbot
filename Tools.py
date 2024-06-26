import re
from typing import List

def divide_sentences(text: str) -> list:
    '''
    切分一段句子
    '''
    sentences = re.findall(r'.*?[~。！？…]+', text)
    if len(sentences) == 0:
        return [text]
    return sentences
