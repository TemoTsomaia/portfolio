from typing import Union


def divide(str_with_ints: str) -> Union[float, str]:
    nums = str_with_ints.split()
    try:
        num1, num2 = nums[0], nums[1]
        return int(num1) / int(num2)
    except Exception as e:
        return f"Error code: {e}"



