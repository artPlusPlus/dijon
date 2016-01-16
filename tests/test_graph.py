import dijon
from dijon import _nodes


def test_graph_initialization():
    graph = dijon.Graph()

    assert isinstance(graph, dijon.Graph)


def test_graph_parse_object():
    data = {'a': 'Foo'}
    graph = dijon.Graph()

    graph.parse(data)

    assert isinstance(graph.root, _nodes.Object)
    assert graph.root.path == 'root'

    for field in graph.root:
        assert isinstance(field, _nodes.ObjectField)
        assert field.path == 'a'
        assert field.value == 'Foo'


def test_graph_parse_sequence():
    data = ['foo']
    graph = dijon.Graph()

    graph.parse(data)

    assert isinstance(graph.root, _nodes.Sequence)
    assert graph.root.path == 'root'

    for item in graph.root:
        assert isinstance(item, _nodes.SequenceItem)
        assert item.value == 'foo'
