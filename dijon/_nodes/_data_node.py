from ._node import Node


class DataNode(Node):
    def __init__(self, path, data):
        super(DataNode, self).__init__(path)

        self.data = data

    def copy(self):
        result = self.__class__(self.path, self.data)
        result.parent = self.parent

        return result

    def __repr__(self):
        result = u"<{0} {{'path': {1}, 'data': {2}}}>"
        result = result.format(self.__class__.__name__,
                               self._repr_path(),
                               repr(self.data))
        return result
