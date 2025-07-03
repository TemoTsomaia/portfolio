from typing import Tuple

def get_tuple(num: int) -> Tuple[int]:
    return tuple(int(digit) for digit in str(abs(num)))

if __name__ == '__main__':
    assert get_tuple(87178291199) == (8, 7, 1, 7, 8, 2, 9, 1, 1, 9, 9)
