import re, json, itertools
from typing import List

def _score_sentence(s: str, seo: List[str]) -> float:
    l = len(s)
    if l > 250:
        return -1
    seo_hit = sum(1 for w in seo if w.lower() in s.lower())
    emoji_pen = -1 if bool(re.search(r'[\U0001F600-\U0001F64F]', s)) else 0
    return (seo_hit * 10) - (l / 10) + emoji_pen

def _split_sentences(text: str) -> List[str]:
    return [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]

def merge_best_versions(texts: List[str],
                        platform: str,
                        seo_words: List[str],
                        max_len: int) -> str:
    """
    texts: 2-3 adet üretilmiş ham metin
    returns: limit içinde en iyi cümlelerin birleşimi
    """
    sentences = [_split_sentences(t) for t in texts]
    consensus = set()
    # aynı cümle 2 farklı metinde varsa otomatik al
    for s1, s2 in itertools.combinations(sentences, 2):
        for c in set(s1) & set(s2):
            consensus.add(c)

    pool = []
    for sent_list in sentences:
        for sent in sent_list:
            if sent in consensus:
                pool.append((sent, 999))  # yüksek skor
            else:
                pool.append((sent, _score_sentence(sent, seo_words)))

    # skora göre sırala
    pool.sort(key=lambda x: x[1], reverse=True)

    out, used = [], set()
    current = 0
    for sent, score in pool:
        if sent in used or score < 0:
            continue
        if current + len(sent) + 1 > max_len:
            break
        out.append(sent)
        used.add(sent)
        current += len(sent) + 1

    text = ". ".join(out) + "."
    # başına ek hashtag
    tags = " ".join([f"#{w.replace(' ', '')}" for w in seo_words[:3]])
    return f"{text}\n\n{tags}"