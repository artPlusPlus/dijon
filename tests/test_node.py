from dijon._nodes._node import Node


def test_node_instantiation():
    node = Node('root')

    assert isinstance(node, Node)
    assert node.path == 'root'
    assert node.full_path == ('root',)
    assert repr(node) == "<Node {'path': root}>"


def test_node_hierarchy():
    root = Node('root')
    child = Node('child')

    child.parent = root

    assert child.parent is root
    assert child.path == 'child'
    assert child.full_path == ('root', 'child')
    assert repr(child) == "<Node {'path': root.child}>"


def test_node_copy():
    node = Node('root')

    copy = node.copy()
    copy.parent = node

    assert isinstance(copy, Node)
    assert copy.path == 'root'
    assert copy.full_path == ('root', 'root')