import logging
from collections import deque

from . import _nodes


_logger = logging.getLogger(__name__)


class Graph(object):
    def __init__(self):
        self.root = None

    def parse(self, json_data):
        _logger.debug("begin parse")

        try:
            self.root = self._parse_object("root", json_data)
        except TypeError:
            self.root = self._parse_sequence("root", json_data)

        _logger.debug("end parse")

        return self.root

    @staticmethod
    def _parse_object(path, data):
        result = _nodes.Object(path, data)

        for field_name in data:
            field_data = data[field_name]
            field = _nodes.ObjectField(field_name, field_data)
            result[field_name] = field

            try:
                field.value = Graph._parse_object(field_name, field_data)
            except TypeError:
                try:
                    field.value = Graph._parse_sequence(field_name, field_data)
                except TypeError:
                    field.value = field_data

        return result

    @staticmethod
    def _parse_sequence(path, data):
        if isinstance(data, str):
            raise TypeError("Unsupported data type: basestring")

        result = _nodes.Sequence(path, data)

        for idx, item_data in enumerate(data):
            item = _nodes.SequenceItem(idx, item_data)
            result.append(item)

            try:
                item.value = Graph._parse_object(idx, item_data)
            except TypeError:
                try:
                    item.value = Graph._parse_sequence(idx, item_data)
                except TypeError:
                    item.value = item_data

        return result

    def iter_nodes(self, data=False, differences=False, conflicts=False):
        nodes = deque([self.root])
        while nodes:
            node = nodes.popleft()
            try:
                nodes.extend(node)
            except TypeError:
                pass

            if not data and isinstance(node, _nodes.DataNode):
                continue
            elif not differences and isinstance(node, _nodes.DifferenceNode):
                continue
            elif not conflicts and isinstance(node, _nodes.ConflictNode):
                continue

            yield node
