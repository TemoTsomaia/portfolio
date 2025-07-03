from typing import List


class Counter:
    def __init__(self, values: List[int]):
        self.values = values


    def __add__(self, other):
        return [f"{i} {other}" for i in self.values]

