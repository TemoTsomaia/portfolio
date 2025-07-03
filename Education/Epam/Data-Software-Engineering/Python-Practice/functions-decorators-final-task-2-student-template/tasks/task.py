from typing import List

def split_by_index(s: str, indexes: List[int]) -> List[str]:
    x = []
    start = 0
    for i in indexes:
        if i >= len(s):
            continue
        x.append(s[start:i])
        start = i

    if start < len(s):
        x.append(s[start:])
    return x


if __name__ == "__main__":
    assert split_by_index("pythoniscool,isn'tit?", [6, 8, 12, 13, 18]) == ["python", "is", "cool", ",", "isn't", "it?"]