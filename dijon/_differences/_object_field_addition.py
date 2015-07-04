from ._difference import Difference


class ObjectFieldAddition(Difference):
    def __init__(self, target_path, target_data):
        super(ObjectFieldAddition, self).__init__(None, None,
                                                  target_path, target_data)
