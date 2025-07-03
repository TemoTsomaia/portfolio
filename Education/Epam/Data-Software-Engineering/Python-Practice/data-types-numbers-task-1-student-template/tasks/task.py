from typing import Union

NumType = Union[int, float]

def some_expression_with_rounding(a: NumType, b: NumType) -> NumType:
  result = None
  result = round((12 * a + 25 * b) / (1 + a**(2**b)), 2)
  return result
