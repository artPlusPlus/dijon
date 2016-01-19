from ._data_node import DataNode


class ObjectField(DataNode):
    def __init__(self, path, data):
        super(ObjectField, self).__init__(path, data)

        self.value = None

    def copy(self):
        result = super(ObjectField, self).copy()
        result.value = self.value

        return result
