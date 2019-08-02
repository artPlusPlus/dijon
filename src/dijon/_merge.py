import logging
from collections import defaultdict

import _nodes
from ._compare import compare
from ._graph import Graph
from ._exceptions import MergeError


_logger = logging.getLogger(__name__)


def merge(ancestor_data, source_data, target_data):
    """
    Merges changes between a source, target, and a common ancestor.

    :param source:
    :param target:
    :param common:
    :return:
    """
    _logger.debug("begin compare")

    result = Graph()

    ancestor_source = compare(ancestor_data, source_data)
    ancestor_target = compare(ancestor_data, target_data)

    if type(ancestor_source.root) is not type(ancestor_target):
        result.root = _nodes.ConflictNode(ancestor_source.root, ancestor_target.root)
    elif isinstance(ancestor_source.root, _nodes.Object):
        result.root = _merge_object(ancestor_source.root, ancestor_target.root)
    elif isinstance(ancestor_data.root, _nodes.Sequence):
        result.root = _merge_sequence(ancestor_source.root, ancestor_target.root)
    else:
        raise MergeError()

    try:
        result.root = _merge_object(ancestor_source, ancestor_target)
    except MergeError:
        result.root = _merge_sequence(ancestor_source, ancestor_target)

    _logger.debug("end compare")
    return result


def _merge_object(ancestor_source, ancestor_target):
    result = _nodes.Object()
    
    all_fields = defaultdict(set)
    
    for field in ancestor_source.fields:
        

    try:
        all_fields = set()
        all_fields.update(ancestor_source.fields)
        all_fields.update(ancestor_target.fields)
    except AttributeError:
        raise MergeError()

    return result


def _compare_object(source, target):
    result = _nodes.Object(target.path, target.data)
    field_pairs = set()

    try:
        all_fields = set()
        all_fields.update(source.keys())
        all_fields.update(target.keys())
    except AttributeError:
        raise ComparisonError()

    for field_name in all_fields:
        src_field = source.get(field_name, None)
        tgt_field = target.get(field_name, None)

        if src_field and tgt_field:
            src_field = src_field.copy()
            tgt_field = tgt_field.copy()
            field_pairs.add((src_field, tgt_field))
        elif src_field:
            src_field = src_field.copy()
            result_field = _nodes.ObjectFieldDeletion(src_field)
            result[src_field.path] = result_field
        elif tgt_field:
            tgt_field = tgt_field.copy()
            result_field = _nodes.ObjectFieldAddition(tgt_field)
            result[tgt_field.path] = result_field

    for src_field, tgt_field in field_pairs:
        try:
            result_value = _compare_object(src_field, tgt_field)
        except ComparisonError:
            try:
                result_value = _compare_sequence(src_field, tgt_field)
            except TypeError:
                result_value = tgt_field.value

        try:
            modified = [isinstance(n, _nodes.DifferenceNode) for n in result_value]
            modified = any(modified)
        except TypeError:
            modified = src_field.value != tgt_field.value

        if modified:
            src_field = src_field.copy()
            tgt_field = tgt_field.copy()
            result_field = _nodes.ObjectFieldModification(src_field, tgt_field)
        else:
            result_field = _nodes.ObjectField(tgt_field.path, tgt_field.data)

        result_field.value = result_value
        result[result_field.path] = result_field

    return result


def _merge_sequence(source, target):
    pass
