from typing import Dict

def combine_dicts(*args:Dict[str, int]) -> Dict[str, int]:
    combined_dicts = {}
    for dictionary in args:
        for letter in dictionary:
            if letter not in combined_dicts:
                combined_dicts[letter] = dictionary[letter]
            else:
                combined_dicts[letter] += dictionary[letter]
    return combined_dicts

dict_1 = {'a': 100, 'b': 200}
dict_2 = {'a': 200, 'c': 300}
dict_3 = {'a': 300, 'd': 100}

if __name__ == "__main__":
    assert combine_dicts(dict_1, dict_2) == {'a': 300, 'b': 200, 'c': 300}
    assert combine_dicts(dict_1, dict_2, dict_3) == {'a': 600, 'b': 200, 'c': 300, 'd': 100}