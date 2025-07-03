from typing import Union, List

ListType = List[Union[int, str]]


def get_fizzbuzz_list(n: int) -> ListType:
    solution = []
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            solution.append("FizzBuzz")
        elif i % 3 == 0:
            solution.append("Fizz")
        elif i % 5 == 0:
            solution.append("Buzz")
        else:
            solution.append(i)
    return solution
