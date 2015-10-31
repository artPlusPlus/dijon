from ._difference import Difference


class SequenceItemAddition(Difference):
    def __init__(self, target_path, target_data):
        super(SequenceItemAddition, self).__init__(None, None,
                                                   target_path, target_data)
