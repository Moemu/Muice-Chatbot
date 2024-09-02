import re


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
