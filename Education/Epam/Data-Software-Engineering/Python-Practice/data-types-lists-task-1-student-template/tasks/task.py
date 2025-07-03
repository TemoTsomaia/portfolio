from typing import List, Tuple

def sort_unique_elements(str_list: Tuple[str, ...]) -> List[str]:
    unique = []
    for i in str_list:
        if i not in unique:
            unique.append(i)
    unique.sort()
    return unique

if __name__ == "__main__":
    assert sort_unique_elements(('red', 'white', 'black', 'red', 'green', 'black')) == ['black', 'green', 'red', 'white']
