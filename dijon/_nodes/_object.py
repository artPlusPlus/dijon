from ._data_node import DataNode
from .._exceptions import ObjectFieldError


class Object(DataNode):
    def __init__(self, path, data):
        super(Object, self).__init__(path, data)

        self._fields = {}

    def __iter__(self):
        for node in self._fields.values():
            yield node

    def __getitem__(self, field_name):
        try:
            return self._fields[field_name]
        except KeyError:
            raise ObjectFieldError()

    def __setitem__(self, field_name, field):
        self._fields[field_name] = field
        field.parent = self

    def __delitem__(self, field_name):
        try:
            del self._fields[field_name]
        except KeyError:
            raise ObjectFieldError()

    def __contains__(self, item):
        return item in self._fields or item in self._fields.values()