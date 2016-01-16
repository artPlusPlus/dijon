import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

from ._graph import Graph

from ._nodes import (
    ObjectFieldAddition,
    ObjectFieldDeletion,
    ObjectFieldModification,
    SequenceItemAddition,
    SequenceItemDeletion,
    SequenceItemIndexChanged,
    SequenceItemValueChanged
)

from ._compare import compare


logging.getLogger(__name__).addHandler(NullHandler())
