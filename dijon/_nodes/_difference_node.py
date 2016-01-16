from ._node import Node


class DifferenceNode(Node):
    def __init__(self, source, target):
        path = (
            source.path if source else None,
            target.path if target else None
        )
        path = path if not all([p == path[0] for p in path]) else path[0]
        super(DifferenceNode, self).__init__(path)

        self.source = source
        self.target = target
