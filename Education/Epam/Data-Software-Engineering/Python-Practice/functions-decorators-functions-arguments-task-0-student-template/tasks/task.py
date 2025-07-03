from typing import Dict

def generate_squares(num: int)-> Dict[int, int]:
    return {i : i**2 for i in range(1, num+1)}

