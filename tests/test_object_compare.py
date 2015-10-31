import dijon


def test_compare_object_no_difference():
    a = {'a': 1, 'b': 2, 'c': 3}
    b = {'a': 1, 'b': 2, 'c': 3}
    differences = dijon.compare(a, b)
    assert len(differences) == 0


def test_compare_field_addition():
    a = {'a': 1, 'b': 2}
    b = {'a': 1, 'b': 2, 'c': 3}

    differences = dijon.compare(a, b)
    assert len(differences) == 1

    difference = differences[0]
    assert isinstance(difference, dijon.ObjectFieldAddition)
    assert difference.target_path == ('root', 'c')
    assert difference.target_data == 3


def test_compare_field_deletion():
    a = {'a': 1, 'b': 2, 'c': 3}
    b = {'a': 1, 'b': 2}

    differences = dijon.compare(a, b)
    assert len(differences) == 1

    difference = differences[0]
    assert isinstance(difference, dijon.ObjectFieldDeletion)
    assert difference.source_path == ('root', 'c')
    assert difference.source_data == 3
