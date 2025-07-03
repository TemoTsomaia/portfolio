class HistoryDict:
    def __init__(self, initial=None):
        self._data = dict(initial) if initial else {}
        self._history = []

    def set_value(self, key, value):
        self._data[key] = value
        if key in self._history:
            self._history.remove(key)
        self._history.append(key)
        if len(self._history) > 5:
            self._history.pop(0)

    def get_history(self):
        return self._history


if __name__ == '__main__':
    d = HistoryDict({"foo": 42})
    d.set_value("bar", 43)
    print(d.get_history())

