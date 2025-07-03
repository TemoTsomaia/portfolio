from typing import Dict


def get_dict(s: str) -> Dict[str, int]:
    s = s.lower()
    solution = {}
    for i in s:
        if i not in solution:
            solution[i] = s.count(i)
    return solution

if __name__ == '__main__':
    assert get_dict('Oh, it is python') == {" ": 3, ",": 1, "h": 2, "i": 2, "n": 1, "o": 2, "p": 1, "s": 1, "t": 2, "y": 1}
