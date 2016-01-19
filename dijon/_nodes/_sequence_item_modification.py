from _difference_node import DifferenceNode


class SequenceItemModification(DifferenceNode):
    def __init__(self, source, target):
        super(SequenceItemModification, self).__init__(source, target)

        self.value = None
