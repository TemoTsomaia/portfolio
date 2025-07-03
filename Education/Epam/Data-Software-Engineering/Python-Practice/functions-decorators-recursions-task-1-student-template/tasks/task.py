from typing import List, Tuple, Union


def seq_sum(sequence: Union[List, Tuple]) -> int:
    tot = 0
    for obj in sequence:
        if isinstance(obj,(list, tuple)):
            tot += seq_sum(obj)
        else:
            tot += obj
    return tot
