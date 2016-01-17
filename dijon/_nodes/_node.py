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

    def __init__(self, path):
        self._parent = None
        self._path = path

    def __iter__(self):
        raise TypeError('Node is not iterable')

    def __repr__(self):
        result = "<{0} {{'path': {1}}}>"
        result = result.format(self.__class__.__name__,
                               '.'.join(self.full_path))
        return result

    def copy(self):
        result = Node(self.path)
        result.parent = self.parent

        return result
