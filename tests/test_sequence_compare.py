import dijon


# def test_compare_sequence_no_difference():
#     a = ['a', 'b', 'c']
#     b = ['a', 'b', 'c']
#     differences = dijon.compare(a, b)
#     assert len(differences) == 0
#
#
# def test_compare_sequence_addition():
#     a = ['a', 'b', 'c']
#
#     b = ['a', 'b', 'c', 'd']
#     differences = dijon.compare(a, b)
#     assert len(differences) == 1
#
#     difference = differences[0]
#     assert isinstance(difference, dijon.SequenceItemAddition)
#     assert difference.target_path == ('root', 3)
#     assert difference.target_data == 'd'
#
#     b = ['z', 'a', 'b', 'c']
#     differences = dijon.compare(a, b)
#     assert len(differences) == 4
#
#     difference = differences[0]
#     assert isinstance(difference, dijon.SequenceItemModification)
#     assert difference.source_path == ('root', 0)
#     assert difference.source_data == 'a'
#     assert difference.target_path == ('root', 1)
#     assert difference.target_data == 'a'
#
#     difference = differences[1]
#     assert isinstance(difference, dijon.SequenceItemModification)
#     assert difference.source_path == ('root', 1)
#     assert difference.source_data == 'b'
#     assert difference.target_path == ('root', 2)
#     assert difference.target_data == 'b'
#
#     difference = differences[2]
#     assert isinstance(difference, dijon.SequenceItemModification)
#     assert difference.source_path == ('root', 2)
#     assert difference.source_data == 'c'
#     assert difference.target_path == ('root', 3)
#     assert difference.target_data == 'c'
#
#     difference = differences[3]
#     assert isinstance(difference, dijon.SequenceItemAddition)
#     assert difference.target_path == ('root', 0)
#     assert difference.target_data == 'z'
#
#     b = ['a', 'b', '7', 'c']
#     differences = dijon.compare(a, b)
#     assert len(differences) == 2
#
#     difference = differences[0]
#     assert isinstance(difference, dijon.SequenceItemModification)
#     assert difference.source_path == ('root', 2)
#     assert difference.source_data == 'c'
#     assert difference.target_path == ('root', 3)
#     assert difference.target_data == 'c'
#
#     difference = differences[1]
#     assert isinstance(difference, dijon.SequenceItemAddition)
#     assert difference.target_path == ('root', 2)
#     assert difference.target_data == '7'
#
#
# def test_compare_sequence_deletion():
#     a = ['a', 'b', 'c']
#
#     b = ['a', 'b']
#     differences = dijon.compare(a, b)
#     assert len(differences) == 1
#
#     difference = differences[0]
#     assert isinstance(difference, dijon.SequenceItemDeletion)
#     assert difference.source_path == ('root', 2)
#     assert difference.source_data == 'c'
#
#     b = ['b', 'c']
#     differences = dijon.compare(a, b)
#     assert len(differences) == 3
#
#     difference = differences[0]
#     assert isinstance(difference, dijon.SequenceItemModification)
#     assert difference.source_path == ('root', 1)
#     assert difference.source_data == 'b'
#     assert difference.target_path == ('root', 0)
#     assert difference.target_data == 'b'
#
#     difference = differences[1]
#     assert isinstance(difference, dijon.SequenceItemModification)
#     assert difference.source_path == ('root', 2)
#     assert difference.source_data == 'c'
#     assert difference.target_path == ('root', 1)
#     assert difference.target_data == 'c'
#
#     difference = differences[2]
#     assert isinstance(difference, dijon.SequenceItemDeletion)
#     assert difference.source_path == ('root', 0)
#     assert difference.source_data == 'a'
#
#     b = ['a', 'c']
#     differences = dijon.compare(a, b)
#     assert len(differences) == 2
#
#     difference = differences[0]
#     assert isinstance(difference, dijon.SequenceItemModification)
#     assert difference.source_path == ('root', 2)
#     assert difference.source_data == 'c'
#     assert difference.target_path == ('root', 1)
#     assert difference.target_data == 'c'
#
#     difference = differences[1]
#     assert isinstance(difference, dijon.SequenceItemDeletion)
#     assert difference.source_path == ('root', 1)
#     assert difference.source_data == 'b'
