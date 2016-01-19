from ._data_node import DataNode
from .._exceptions import SequenceItemError


class Sequence(DataNode):
    def __init__(self, path, data):
        super(Sequence, self).__init__(path, data)

        self._items = []

    def __iter__(self):
        for node in self._items:
            yield node

    def __getitem__(self, item_index):
        try:
            return self._items[item_index]
        except IndexError:
            raise SequenceItemError()

    def __setitem__(self, item_index, item):
        self._items[item_index] = item
        item.parent = self

    def append(self, item):
        self._items.append(item)
        item.parent = self

    def insert(self, index, item):
        self._items.insert(index, item)
        item.parent = self

    def __len__(self):
        return len(self._items)