from ._node import Node


class DifferenceNode(Node):
    def __init__(self, source, target):
        path = (
            source.path if source else None,
            target.path if target else None
        )
        super(DifferenceNode, self).__init__(path)

        self.source = source
        if self.source:
            self.source.parent = self

        self.target = target
        if self.target:
            self.target.parent = self

    def copy(self):
        result = self.__class__(self.source, self.target)
        result.parent = self.parent

        return result

    def __repr__(self):
        result = u"<{0} {{'path': {1}, 'source': {2}, 'target': {3}}}>"
        result = result.format(self.__class__.__name__,
                               self._repr_path(),
                               repr(self.source),
                               repr(self.target))
        return result
