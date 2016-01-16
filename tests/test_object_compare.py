import dijon


def test_compare_object_no_difference():
    source_data = {'a': 1, 'b': 2, 'c': 3}
    target_data = {'a': 1, 'b': 2, 'c': 3}

    diff_graph = dijon.compare(source_data, target_data)
    diff_nodes = [n for n in diff_graph.iter_nodes(differences=True)]
    assert len(diff_nodes) == 0


def test_compare_field_addition():
    source_data = {'a': 1, 'b': 2}
    target_data = {'a': 1, 'b': 2, 'c': 3}

    diff_graph = dijon.compare(source_data, target_data)
    diff_nodes = [n for n in diff_graph.iter_nodes(differences=True)]
    assert len(diff_nodes) == 1

    difference = diff_nodes[0]
    assert isinstance(difference, dijon.ObjectFieldAddition)
    assert difference.target.full_path == ('c',)
    assert difference.target.data == 3


def test_compare_field_deletion():
    source_data = {'a': 1, 'b': 2, 'c': 3}
    target_data = {'a': 1, 'b': 2}

    diff_graph = dijon.compare(source_data, target_data)
    diff_nodes = [n for n in diff_graph.iter_nodes(differences=True)]
    assert len(diff_nodes) == 1

    difference = diff_nodes[0]
    assert isinstance(difference, dijon.ObjectFieldDeletion)
    assert difference.source.full_path == ('c',)
    assert difference.source.data == 3


def test_compare_field_modification():
    source_data = {'a': 1, 'b': 2, 'c': 3}
    target_data = {'a': 1, 'b': 2, 'c': 5}

    diff_graph = dijon.compare(source_data, target_data)
    diff_nodes = [n for n in diff_graph.iter_nodes(differences=True)]
    assert len(diff_nodes) == 1

    difference = diff_nodes[0]
    assert isinstance(difference, dijon.ObjectFieldModification)
    assert difference.source.full_path == ('c',)
    assert difference.source.data == 3
    assert difference.target.full_path == ('c',)
    assert difference.target.data == 5
