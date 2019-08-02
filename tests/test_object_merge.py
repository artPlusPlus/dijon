import dijon


def test_merge_object_no_difference():
    common_data = {"a": 1, "b": 2, "c": 3}
    source_data = {"a": 1, "b": 2, "c": 3}
    target_data = {"a": 1, "b": 2, "c": 3}

    merge_graph = dijon.merge(source_data, target_data)
    conflict_nodes = [n for n in diff_graph.iter_nodes()]
    assert len(diff_nodes) == 0


def test_compare_object_field_addition():
    source_data = {"a": 1, "b": 2}
    target_data = {"a": 1, "b": 2, "c": 3}

    diff_graph = dijon.compare(source_data, target_data)
    diff_nodes = [n for n in diff_graph.iter_nodes(differences=True)]
    assert len(diff_nodes) == 1

    difference = diff_nodes[0]
    assert isinstance(difference, dijon.ObjectFieldAddition)
    assert difference.full_path == ("root", (None, "c"))
    assert difference.source is None
    assert difference.target.full_path == ("root", (None, "c"), "c")
    assert difference.target.data == 3
