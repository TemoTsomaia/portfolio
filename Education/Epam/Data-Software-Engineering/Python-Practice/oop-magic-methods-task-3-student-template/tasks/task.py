from __future__ import annotations
from typing import Type


class Currency:
    code = None
    _cur = {
        "EUR" : 1.0,
        "USD" : 2.0,
        "GBP" : 100.0
    }

    def __init__(self, value: float):
        self.value = value

    @classmethod
    def course(cls, other_cls: Type[Currency]) -> str:
        first = cls._cur[cls.code]
        second = cls._cur[other_cls.code]
        return f"{second / first} {other_cls.code} for 1 {cls.code}"


    def to_currency(self, other_cls: Type[Currency]):
        first = self._cur[self.code]
        second = other_cls._cur[other_cls.code]
        return other_cls(self.value * (second / first))


    def __add__(self, other):
        if not isinstance(other, Currency):
            raise TypeError("Can not use '+' between currency and not currency types")
        revalueted = other.to_currency(self.__class__)
        return self.__class__(self.value + revalueted.value)

    def __eq__(self, other):
        if not isinstance(other, Currency):
            raise TypeError("Can not use '+' between currency and not currency types")
        return self.to_currency(Dollar).value == other.to_currency(Dollar).value

    def __lt__(self, other):
        if not isinstance(other, Currency):
            return TypeError("Can not use '+' between currency and not currency types")
        return self.to_currency(Dollar).value < other.to_currency(Dollar).value

    def __gt__(self, other):
        if not isinstance(other, Currency):
            return TypeError("Can not use '+' between currency and not currency types")
        return self.to_currency(Dollar).value > other.to_currency(Dollar).value

    def __str__(self):
        return f"{self.value} {self.code}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"



class Euro(Currency):
    code = "EUR"

class Dollar(Currency):
    code = "USD"

class Pound(Currency):
    code = "GBP"

