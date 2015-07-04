from ._difference import Difference


class ObjectFieldDeletion(Difference):
    def __init__(self, source_path, source_data):
        super(ObjectFieldDeletion, self).__init__(source_path, source_data,
                                                  None, None)
