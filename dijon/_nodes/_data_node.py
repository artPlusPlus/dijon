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
        full_path = []
        for item in self.full_path:
            if isinstance(item, (list, tuple, set)):
                item = '|'.join(item)
                item = '[{0}]'.format(item)
            full_path.append(item)
        full_path = '.'.join(full_path)

        result = "<{0} {{'path': {1}, 'data': {2}}}>"
        result = result.format(self.__class__.__name__,
                               full_path,
                               repr(self.data))
        return result
