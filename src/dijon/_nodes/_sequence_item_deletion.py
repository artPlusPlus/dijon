from ._difference_node import DifferenceNode


class SequenceItemDeletion(DifferenceNode):
    def __init__(self, source):
        super(SequenceItemDeletion, self).__init__(source, None)

        self.value = None
