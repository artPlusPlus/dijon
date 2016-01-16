import logging

from ._data_node import DataNode


_logger = logging.getLogger(__name__)


class SequenceItem(DataNode):
    def __init__(self, path, data):
        super(SequenceItem, self).__init__(path, data)

        self.value = None
