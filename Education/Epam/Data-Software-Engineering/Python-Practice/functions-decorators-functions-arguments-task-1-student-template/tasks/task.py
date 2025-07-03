from typing import Dict, Any, Callable, Iterable

DataType = Iterable[Dict[str, Any]]
ModifierFunc = Callable[[DataType], DataType]


def query(data: DataType, selector: ModifierFunc,
          *filters: ModifierFunc) -> DataType:
    for f in filters:
        data = f(data)
    return selector(data)


def select(*columns: str) -> ModifierFunc:
    def modifier(data: DataType) -> DataType:
        return [
            {col: row[col] for col in columns if col in row}
            for row in data
        ]
    return modifier

def field_filter(column: str, *values: Any) -> ModifierFunc:
    def filter(data: DataType) -> DataType:
        return [
            row for row in data if row.get(column) in values
        ]
    return filter


def test_query():
    friends = [
        {'name': 'Sam', 'gender': 'male', 'sport': 'Basketball'}
    ]
    value = query(
        friends,
        select(*('name', 'gender', 'sport')),
        field_filter(*('sport', *('Basketball', 'volleyball'))),
        field_filter(*('gender', *('male',))),
    )
    assert [{'gender': 'male', 'name': 'Sam', 'sport': 'Basketball'}] == value


if __name__ == "__main__":
    test_query()

