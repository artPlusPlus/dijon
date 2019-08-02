from ._node import Node


class ConflictNode(Node):
    @property
    def resolved(self):
        return isinstance(self.resolve_node, Node)

    def __init__(self, path, source_node, target_node):
        super().__init__(path)

        self.source_node = source_node
        self.target_node = target_node
        self.resolve_node = None

    def resolve(self, node):
        self.resolve_node = node
