class CustomList:
    def __init__(self):
        self._data = []

    def __getitem__(self, index):
        return self._data[index]

    def __iadd__(self, other):
        self._data.append(other)
        return self

