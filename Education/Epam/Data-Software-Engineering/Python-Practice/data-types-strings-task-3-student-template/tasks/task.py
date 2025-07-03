def replacer(s: str) -> str:
    x = ""
    for i in s:
        match i:
            case '\"':
                x += "\'"
            case "\'":
                x += '\"'
            case _:
                x += i
    return x

if __name__ == "__main__":
    assert replacer("\'hello world") == "\"hello world"
    assert replacer("\"hello world") == "\'hello world"
    assert replacer("\"hello world\'") == "\'hello world\""