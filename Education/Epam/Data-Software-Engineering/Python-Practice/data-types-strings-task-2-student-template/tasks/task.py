def get_longest_word( s: str) -> str:
    words = s.split()
    result = max(words, key=len)
    return result

if __name__ == '__main__':
    assert get_longest_word('Python is simple and effective!') == 'effective!'
