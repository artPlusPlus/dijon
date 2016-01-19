from _difference_node import DifferenceNode


class ObjectFieldModification(DifferenceNode):
    def __init__(self, source, target):
        super(ObjectFieldModification, self).__init__(source, target)
