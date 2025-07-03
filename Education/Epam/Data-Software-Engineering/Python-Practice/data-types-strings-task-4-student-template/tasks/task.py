def check_str(s: str):
    sl = s.lower()
    x = ""
    for i in sl:
        if i.isalnum():
            x += i
    return x == x[::-1]
