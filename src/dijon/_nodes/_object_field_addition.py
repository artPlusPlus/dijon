from ._difference_node import DifferenceNode


class ObjectFieldAddition(DifferenceNode):
    def __init__(self, target):
        super(ObjectFieldAddition, self).__init__(None, target)
