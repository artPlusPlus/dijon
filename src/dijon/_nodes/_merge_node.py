from ._node import Node


class MergeNode(Node):
    def __init__(self, path, ancestor_source_node, ancestor_target_node):
        super().__init__(path)

        self.ancestor_source_node = ancestor_source_node
        self.ancestor_target_node = ancestor_target_node
