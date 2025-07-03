from typing import List


def foo(nums: List[int]) -> List[int]:
    solution = []
    for i in range(len(nums)):

        x = 1

        for j in range(len(nums)):
            if i != j:
                x *= nums[j]

        solution.append(x)

    return solution

if __name__ == '__main__':
    assert foo([1, 2, 3, 4, 5]) == [120, 60, 40, 30, 24]
    assert foo([3, 2, 1]) == [2, 3, 6]