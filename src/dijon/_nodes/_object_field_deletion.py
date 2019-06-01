from ._difference_node import DifferenceNode


class ObjectFieldDeletion(DifferenceNode):
    def __init__(self, source):
        super(ObjectFieldDeletion, self).__init__(source, None)
