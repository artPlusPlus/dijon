from _difference_node import DifferenceNode


class SequenceItemIndexChanged(DifferenceNode):
    def __init__(self, source, target):
        super(SequenceItemIndexChanged, self).__init__(source, target)

        self.value = None
