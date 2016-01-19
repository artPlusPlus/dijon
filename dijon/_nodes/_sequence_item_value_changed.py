from _difference_node import DifferenceNode


class SequenceItemValueChanged(DifferenceNode):
    def __init__(self, source, target):
        super(SequenceItemValueChanged, self).__init__(source, target)

        self.value = None
