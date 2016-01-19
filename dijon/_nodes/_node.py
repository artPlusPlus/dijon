import weakref


class Node(object):
    @property
    def parent(self):
        try:
            return self._parent()
        except TypeError:
            return None

    @parent.setter
    def parent(self, value):
        try:
            self._parent = weakref.ref(value)
        except TypeError:
            self._parent = value

    @property
    def path(self):
        return self._path

    @property
    def full_path(self):
        result = list(self.parent.full_path) if self.parent else []
        result.append(self._path)
        result = tuple(result)
        return result

    def copy(self):
        result = Node(self.path)
        result.parent = self.parent

        return result

    def __init__(self, path):
        self._parent = None
        self._path = path

    def __iter__(self):
        raise TypeError('Node is not iterable')

    def __repr__(self):
        result = "<{0} {{'path': {1}}}>"
        result = result.format(self.__class__.__name__,
                               self._repr_path())
        return result

    def _repr_path(self):
        result = []

        for item in self.full_path:
            if isinstance(item, (list, tuple, set)):
                item = u'|'.join([str(i) for i in item])
                item = u'[{0}]'.format(item)
            result.append(item)

        result = u'.'.join([unicode(r) for r in result])

        return result
