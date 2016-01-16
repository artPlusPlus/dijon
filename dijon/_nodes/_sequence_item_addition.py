from _difference_node import DifferenceNode


class SequenceItemAddition(DifferenceNode):
    def __init__(self, target):
        super(SequenceItemAddition, self).__init__(None, target)
