def union(*args) -> set:
    x = set()
    for i in args:
        for j in i:
            if j not in x:
                x.add(j)
    return x


def intersect(*args) -> set:
    x = set()
    for i in args[0]:
        everywhere = True
        for j in args[1:]:
            if i not in j:
                everywhere = False
                break
        if everywhere and i not in x:
            x.add(i)
    return x


if __name__ == '__main__':
    assert union(('S', 'A', 'M'), ['S', 'P', 'A', 'C']) == {'S', 'P', 'A', 'M', 'C'}
    assert intersect(('S', 'A', 'C'), ('P', 'C', 'S'), ('G', 'H', 'S', 'C')) == {'S', 'C'}
