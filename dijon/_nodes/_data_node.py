from ._node import Node


class DataNode(Node):
    def __init__(self, path, data):
        super(DataNode, self).__init__(path)

        self.data = data
