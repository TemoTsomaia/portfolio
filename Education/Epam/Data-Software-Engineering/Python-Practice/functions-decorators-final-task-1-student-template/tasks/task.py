from typing import List

from typing import List

def split(data: str, sep=None, maxsplit=-1) -> List[str]:
    result = []

    if sep is None:
        data = data.strip()
        if maxsplit == 0:
            return [data] if data else []
        i = 0
        length = len(data)
        splits = 0
        while i < length:
            # Skip whitespace
            while i < length and data[i].isspace():
                i += 1
            if i >= length:
                break
            start = i
            while i < length and not data[i].isspace():
                i += 1
            result.append(data[start:i])
            splits += 1
            if 0 <= maxsplit == splits:
                break
        if 0 <= maxsplit == splits and i < length:
            while i < length and data[i].isspace():
                i += 1
            if i < length:
                result.append(data[i:])
        return result

    else:
        if maxsplit == 0:
            return [data]
        sep_len = len(sep)
        start = 0
        splits = 0
        i = 0
        while i <= len(data) - sep_len:
            if data[i:i+sep_len] == sep and (maxsplit == -1 or splits < maxsplit):
                result.append(data[start:i])
                i += sep_len
                start = i
                splits += 1
            else:
                i += 1
        result.append(data[start:])
        return result



if __name__ == '__main__':

    assert split(',123,', sep=',') == ['', '123', '']
    assert split('test') == ['test']
    assert split('Python    2     3', maxsplit=1) == ['Python', '2     3']
    assert split('    test     6    7', maxsplit=1) == ['test', '6    7']
    assert split('    Hi     8    9', maxsplit=0) == ['Hi     8    9']
    assert split('    set   3     4') == ['set', '3', '4']
    assert split('set;:23', sep=';:', maxsplit=0) == ['set;:23']
    assert split('set;:;:23', sep=';:', maxsplit=2) == ['set', '', '23']