from typing import Any, List

def linear_seq(sequence: List[Any]) -> List[Any]:
    x = []
    for obj in sequence:
        if isinstance(obj, (list, tuple)):
            x.extend(linear_seq(obj))
        else:
            x.append(obj)
    return x
