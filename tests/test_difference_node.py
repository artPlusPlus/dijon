from dijon._nodes._data_node import DataNode
from dijon._nodes._difference_node import DifferenceNode


def test_differencenode_initialization():
    source_data = {'foo': 'bar'}
    source_node = DataNode('root', source_data)

    target_data = {'bar': 'foo'}
    target_node = DataNode('root', target_data)

    node = DifferenceNode(source_node, target_node)

    assert isinstance(node, DifferenceNode)
    assert node.path == ('root', 'root')
    assert node.full_path == (('root', 'root'),)

    diff_repr = "<DifferenceNode {{'path': [root|root], 'source': {0}, 'target': {1}}}>"
    diff_repr = diff_repr.format(repr(source_node), repr(target_node))
    assert repr(node) == diff_repr


def test_differencenode_copy():
    source_data = {'foo': 'bar'}
    source_node = DataNode('root', source_data)

    target_data = {'bar': 'foo'}
    target_node = DataNode('root', target_data)

    node = DifferenceNode(source_node, target_node)

    copy = node.copy()
    copy.parent = node

    assert isinstance(copy, DifferenceNode)
    assert node is not copy
    assert copy.path == ('root', 'root')
    assert copy.full_path == (('root', 'root'), ('root', 'root'))
    assert copy.source == node.source
    assert copy.target == node.target
