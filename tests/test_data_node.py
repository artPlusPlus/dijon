from dijon._nodes._data_node import DataNode


def test_datanode_initialization():
    data = {'foo': 'bar'}
    node = DataNode('root', data)

    assert isinstance(node, DataNode)
    assert node.path == 'root'
    assert node.full_path == ('root',)

    data_repr = "<DataNode {{'path': root, 'data': {0}}}>"
    data_repr = data_repr.format(repr(data))
    assert repr(node) == data_repr


def test_datanode_copy():
    data = {'foo': 'bar'}
    node = DataNode('root', data)

    copy = node.copy()
    copy.parent = node

    assert isinstance(copy, DataNode)
    assert node is not copy
    assert copy.path == 'root'
    assert copy.full_path == ('root', 'root')
    assert copy.data == node.data
