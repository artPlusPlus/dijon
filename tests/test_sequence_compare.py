import dijon


def test_compare_sequence_no_difference():
    source_data = ['a', 'b', 'c']
    target_data = ['a', 'b', 'c']

    diff_graph = dijon.compare(source_data, target_data)
    diff_nodes = [n for n in diff_graph.iter_nodes(differences=True)]
    assert len(diff_nodes) == 0


def test_compare_sequence_append():
    source_data = ['a', 'b', 'c']
    target_data = ['a', 'b', 'c', 'd']

    diff_graph = dijon.compare(source_data, target_data)
    diff_nodes = [n for n in diff_graph.iter_nodes(differences=True)]
    assert len(diff_nodes) == 1

    difference = diff_nodes[0]
    assert isinstance(difference, dijon.SequenceItemAddition)
    assert difference.full_path == ('root', (None, 3))
    assert difference.source is None
    assert difference.target.full_path == ('root', (None, 3), 3)
    assert difference.target.value == 'd'


def test_compare_sequence_insert():
    source_data = ['a', 'b', 'c']
    target_data = ['z', 'a', 'b', 'c']

    diff_graph = dijon.compare(source_data, target_data)
    diff_nodes = [n for n in diff_graph.iter_nodes(differences=True)]
    assert len(diff_nodes) == 4

    difference = diff_nodes[0]
    assert isinstance(difference, dijon.SequenceItemModification)
    assert difference.full_path == ('root', (0, 1))
    assert difference.source.full_path == ('root', (0, 1), 0)
    assert difference.source.data == 'a'
    assert difference.target.full_path == ('root', (0, 1), 1)
    assert difference.target.data == 'a'

    difference = diff_nodes[1]
    assert isinstance(difference, dijon.SequenceItemModification)
    assert difference.full_path == ('root', (1, 2))
    assert difference.source.full_path == ('root', (1, 2), 1)
    assert difference.source.data == 'b'
    assert difference.target.full_path == ('root', (1, 2), 2)
    assert difference.target.data == 'b'

    difference = diff_nodes[2]
    assert isinstance(difference, dijon.SequenceItemModification)
    assert difference.full_path == ('root', (2, 3))
    assert difference.source.full_path == ('root', (2, 3), 2)
    assert difference.source.data == 'c'
    assert difference.target.full_path == ('root', (2, 3), 3)
    assert difference.target.data == 'c'

    difference = diff_nodes[3]
    assert isinstance(difference, dijon.SequenceItemAddition)
    assert difference.full_path == ('root', (None, 0))
    assert difference.source is None
    assert difference.target.full_path == ('root', (None, 0), 0)
    assert difference.target.data == 'z'

    target_data = ['a', 'b', 'z', 'c']

    diff_graph = dijon.compare(source_data, target_data)
    diff_nodes = [n for n in diff_graph.iter_nodes(differences=True)]
    assert len(diff_nodes) == 2

    difference = diff_nodes[0]
    assert isinstance(difference, dijon.SequenceItemModification)
    assert difference.full_path == ('root', (2, 3))
    assert difference.source.full_path == ('root', (2, 3), 2)
    assert difference.source.data == 'c'
    assert difference.target.full_path == ('root', (2, 3), 3)
    assert difference.target.data == 'c'

    difference = diff_nodes[1]
    assert isinstance(difference, dijon.SequenceItemAddition)
    assert difference.full_path == ('root', (None, 2))
    assert difference.source is None
    assert difference.target.full_path == ('root', (None, 2), 2)
    assert difference.target.data == 'z'


def test_compare_sequence_deletion():
    source_data = ['a', 'b', 'c']
    target_data = ['a', 'b']

    diff_graph = dijon.compare(source_data, target_data)
    diff_nodes = [n for n in diff_graph.iter_nodes(differences=True)]
    assert len(diff_nodes) == 1

    difference = diff_nodes[0]
    assert isinstance(difference, dijon.SequenceItemDeletion)
    assert difference.full_path == ('root', (2, None))
    assert difference.source.full_path == ('root', (2, None), 2)
    assert difference.source.data == 'c'
    assert difference.target is None

    target_data = ['b', 'c']

    diff_graph = dijon.compare(source_data, target_data)
    diff_nodes = [n for n in diff_graph.iter_nodes(differences=True)]
    assert len(diff_nodes) == 3

    difference = diff_nodes[0]
    assert isinstance(difference, dijon.SequenceItemModification)
    assert difference.full_path == ('root', (1, 0))
    assert difference.source.full_path == ('root', (1, 0), 1)
    assert difference.source.data == 'b'
    assert difference.target.full_path == ('root', (1, 0), 0)
    assert difference.target.data == 'b'

    difference = diff_nodes[1]
    assert isinstance(difference, dijon.SequenceItemModification)
    assert difference.full_path == ('root', (2, 1))
    assert difference.source.full_path == ('root', (2, 1), 2)
    assert difference.source.data == 'c'
    assert difference.target.full_path == ('root', (2, 1), 1)
    assert difference.target.data == 'c'

    difference = diff_nodes[2]
    assert isinstance(difference, dijon.SequenceItemDeletion)
    assert difference.full_path == ('root', (0, None))
    assert difference.source.full_path == ('root', (0, None), 0)
    assert difference.source.data == 'a'
    assert difference.target is None

    target_data = ['a', 'c']

    diff_graph = dijon.compare(source_data, target_data)
    diff_nodes = [n for n in diff_graph.iter_nodes(differences=True)]
    assert len(diff_nodes) == 2

    difference = diff_nodes[0]
    assert isinstance(difference, dijon.SequenceItemModification)
    assert difference.full_path == ('root', (2, 1))
    assert difference.source.full_path == ('root', (2, 1), 2)
    assert difference.source.data == 'c'
    assert difference.target.full_path == ('root', (2, 1), 1)
    assert difference.target.data == 'c'

    difference = diff_nodes[1]
    assert isinstance(difference, dijon.SequenceItemDeletion)
    assert difference.full_path == ('root', (1, None))
    assert difference.source.full_path == ('root', (1, None), 1)
    assert difference.source.data == 'b'
    assert difference.target is None
