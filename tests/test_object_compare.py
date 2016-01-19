import dijon


def test_compare_object_no_difference():
    source_data = {'a': 1, 'b': 2, 'c': 3}
    target_data = {'a': 1, 'b': 2, 'c': 3}

    diff_graph = dijon.compare(source_data, target_data)
    diff_nodes = [n for n in diff_graph.iter_nodes(differences=True)]
    assert len(diff_nodes) == 0


def test_compare_object_field_addition():
    source_data = {'a': 1, 'b': 2}
    target_data = {'a': 1, 'b': 2, 'c': 3}

    diff_graph = dijon.compare(source_data, target_data)
    diff_nodes = [n for n in diff_graph.iter_nodes(differences=True)]
    assert len(diff_nodes) == 1

    difference = diff_nodes[0]
    assert isinstance(difference, dijon.ObjectFieldAddition)
    assert difference.full_path == ('root', (None, 'c'))
    assert difference.source is None
    assert difference.target.full_path == ('root', (None, 'c'), 'c')
    assert difference.target.data == 3


def test_compare_object_field_deletion():
    source_data = {'a': 1, 'b': 2, 'c': 3}
    target_data = {'a': 1, 'b': 2}

    diff_graph = dijon.compare(source_data, target_data)
    diff_nodes = [n for n in diff_graph.iter_nodes(differences=True)]
    assert len(diff_nodes) == 1

    difference = diff_nodes[0]
    assert isinstance(difference, dijon.ObjectFieldDeletion)
    assert difference.full_path == ('root', ('c', None))
    assert difference.source.full_path == ('root', ('c', None), 'c')
    assert difference.source.data == 3
    assert difference.target is None


def test_compare_object_field_modification():
    source_data = {'a': 1, 'b': 2, 'c': 3}
    target_data = {'a': 1, 'b': 2, 'c': 5}

    diff_graph = dijon.compare(source_data, target_data)
    diff_nodes = [n for n in diff_graph.iter_nodes(differences=True)]
    assert len(diff_nodes) == 1

    difference = diff_nodes[0]
    assert isinstance(difference, dijon.ObjectFieldModification)
    assert difference.full_path == ('root', ('c', 'c'))
    assert difference.source.full_path == ('root', ('c', 'c'), 'c')
    assert difference.source.data == 3
    assert difference.target.full_path == ('root', ('c', 'c'), 'c')
    assert difference.target.data == 5
