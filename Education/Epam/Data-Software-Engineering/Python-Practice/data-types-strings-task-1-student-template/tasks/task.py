def get_fractions(a_b: str, c_b: str) -> str:
    split1 = a_b.split('/')
    split2 = c_b.split('/')
    result = f"{a_b} + {c_b} = {int(split1[0]) + int(split2[0])}/{int(split1[1])}"
    return result


if __name__ == "__main__":
    assert get_fractions("3/5", '5/5') == "3/5 + 5/5 = 8/5"
