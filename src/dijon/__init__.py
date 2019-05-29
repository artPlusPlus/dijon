import logging
try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())


from ._graph import Graph

from ._nodes import (
    ObjectFieldAddition,
    ObjectFieldDeletion,
    ObjectFieldModification,
    SequenceItemAddition,
    SequenceItemDeletion,
    SequenceItemModification
)

from ._compare import compare
