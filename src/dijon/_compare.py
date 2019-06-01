import logging

from . import _nodes
from ._graph import Graph
from ._exceptions import ComparisonError


_logger = logging.getLogger(__name__)


def compare(source_data, target_data):
    """
    compare identifies differences between two JSON structures.

    :param source_data: The "left" side of the comparison
    :param target_data: The "right" side of the comparison
    :return: Returns a graph
    """
    _logger.debug("begin compare")

    result = Graph()

    source = Graph()
    source.parse(source_data)

    target = Graph()
    target.parse(target_data)

    try:
        result.root = _compare_object(source.root, target.root)
    except ComparisonError:
        result.root = _compare_sequence(source.root, target.root)

    _logger.debug("end compare")
    return result


def _compare_object(source, target):
    try:
        all_fields = set()
        all_fields.update(source.keys())
        all_fields.update(target.keys())
    except AttributeError:
        raise ComparisonError()

    result = _nodes.Object(target.path, target.data)
    field_pairs = set()

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


def _compare_sequence(source, target, match_threshold=0.1):
    if isinstance(source, str):
        raise TypeError("Unsupported source type: basestring")
    elif isinstance(target, str):
        raise TypeError("Unsupported target type: basestring")

    result = _nodes.Sequence(target.path, target.data)

    match_data = _compute_sequence_item_matches(source.data, target.data)
    matched_src_indices = []
    matched_tgt_indices = []

    # Handle modified Items
    for src_idx, tgt_idx, match_hits, match_misses in match_data:
        src_item = source[src_idx]
        tgt_item = target[tgt_idx]

        # Discard the match if average hits is below threshold
        if match_hits / (match_hits + match_misses) < match_threshold:
            result_item = _nodes.SequenceItemDeletion(src_item)
            result.append(result_item)

            result_item = _nodes.SequenceItemAddition(tgt_item)
            result.append(result_item)
            continue

        # At this point, src_item and tgt_item are considered a match
        matched_src_indices.append(src_idx)
        matched_tgt_indices.append(tgt_idx)

        try:
            result_value = _compare_object(src_item, tgt_item)
        except ComparisonError:
            try:
                result_value = _compare_sequence(src_item, tgt_item)
            except TypeError:
                result_value = tgt_item.value

        modified = src_item.path != tgt_item.path
        if not modified:
            try:
                modified = [isinstance(n, _nodes.DifferenceNode) for n in result_value]
                modified = any(modified)
            except TypeError:
                modified = src_item.value != tgt_item.value

        if modified:
            src_item = src_item.copy()
            tgt_item = tgt_item.copy()
            result_item = _nodes.SequenceItemModification(src_item, tgt_item)
        else:
            result_item = _nodes.SequenceItem(tgt_item.path, tgt_item.data)

        result_item.value = result_value
        result.append(result_item)

    # Handle deleted Items
    for src_idx in range(0, len(source)):
        if src_idx in matched_src_indices:
            continue

        diff = _nodes.SequenceItemDeletion(source[src_idx].copy())
        result.append(diff)

    # Handle added Items
    for tgt_idx in range(0, len(target)):
        if tgt_idx in matched_tgt_indices:
            continue

        diff = _nodes.SequenceItemAddition(target[tgt_idx].copy())
        result.append(diff)

    return result


def _compute_sequence_item_matches(source_sequence, target_sequence):
    """
    Matches items from a source sequence to similar items in a target sequence.

    :param source_sequence:
    :param target_sequence:
    :return:
    """
    result = []

    len_source = len(source_sequence)
    len_target = len(target_sequence)
    num_matches = len_source if len_source < len_target else len_target

    # Rank each target item against each source item.
    # Each source item will have a list containing all the items in the
    # target sequence.
    match_candidates = {}
    for src_idx, src_item in enumerate(source_sequence):
        tgt_candidates = _compute_sequence_item_match_candidates(src_item, target_sequence)
        match_candidates[src_idx] = tgt_candidates

    # Compute the best target item match for each source item.
    # It's possible for multiple source items to be similar the same target
    # item.
    # This loop ensures the highest scoring source-target pairs are matched.
    matches = {}
    while len(matches) < num_matches and match_candidates:
        # Each iteration pops the top-scoring target item for each source item.
        round_picks = []
        for src_idx, tgt_candidates in match_candidates.items():
            round_pick = tgt_candidates.pop(0)
            round_picks.append((round_pick.score, src_idx, round_pick))

        # The picks are sorted so a source-target pair with a higher similarity
        # is matched before another source-target that shares the same target.
        round_picks.sort()
        round_picks.reverse()

        # Create matches between unclaimed target items and source items.
        for _, src_idx, candidate in round_picks:
            if candidate.target_index in matches:
                # Target item has already been matched to a higher-scoring
                # (more similar) source item. The next iteration round will
                # attempt to match the source item with the next best target
                # item.
                continue
            matches[candidate.target_index] = (src_idx, candidate)
            del match_candidates[src_idx]

    for src_idx, match in matches.values():
        result.append((src_idx, match.target_index, match.hits, match.misses))

    result = sorted(result)

    return result


def _compute_sequence_item_match_candidates(source_item, target_items):
    """
    Ranks target items based on similarity to the source item.

    :param source_item:
    :param target_items:
    :return:
    """
    result = []

    for target_idx, target_item in enumerate(target_items):
        target_score = _compute_item_similarity(source_item, target_item)

        candidate = _TargetSequenceMatchCandidate()
        candidate.target_index = target_idx
        candidate.hits, candidate.misses = target_score

        result.append(candidate)

    result.sort()
    result.reverse()

    # TODO: Handle candidate_indices with same score
    return result


def _compute_item_similarity(source, target):
    """
    Calculates a score representing how closely two values match each other.

    The score is represented by two integers. The first is "hits", or the number
    if common pieces of data. The second is "misses", or the number of differing
    pieces of data.

    :param source:
    :param target:
    :return:
    """
    try:
        return _compute_object_score(source, target)
    except TypeError:
        try:
            return _compute_sequence_score(source, target)
        except TypeError:
            return float(source == target), float(source != target)


def _compute_sequence_score(source, target):
    """
    Calculates a score representing how closely two sequences match each other.

    :param source:
    :param target:
    :return:
    """
    if isinstance(source, str):
        raise TypeError("Unsupported source type: basestring")
    elif isinstance(target, str):
        raise TypeError("Unsupported target type: basestring")

    hits = 0.0
    misses = abs(len(source) - len(target)) * 2.0

    item_matches = _compute_sequence_item_matches(source, target)

    for src_idx, tgt_idx, match_hits, match_misses in item_matches:
        hits += match_hits
        misses += match_misses
        if src_idx == tgt_idx:
            hits += 1
        else:
            misses += 1

    return hits, misses


def _compute_object_score(source, target):
    """
    Calculates a score representing how closely two objects match each other.

    The calculation compares both keys and values. A missing key counts as
    both a missing key and a missing value.
    :param source:
    :param target:
    :return: Percentage
    """
    hits = 0.0
    misses = 0.0

    try:
        src_keys = source.keys()
    except AttributeError:
        raise TypeError("Unsupported source type: {0}".format(source.__class__))
    try:
        tgt_keys = target.keys()
    except AttributeError:
        raise TypeError("Unsupported target type: {0}".format(target.__class__))

    common_keys = set(src_keys).intersection(tgt_keys)
    missing_source_keys = set(tgt_keys).difference(src_keys)
    missing_target_keys = set(src_keys).difference(tgt_keys)

    misses += len(missing_source_keys) * 2
    misses += len(missing_target_keys) * 2

    for key in common_keys:
        hits += 1

        value_hits, value_misses = _compute_item_similarity(source[key], target[key])
        hits += value_hits
        misses += value_misses

    return hits, misses


class _TargetSequenceMatchCandidate(object):
    target_index = 0
    hits = 0.0
    misses = 0.0

    @property
    def score(self):
        try:
            return self.hits / (self.hits + self.misses)
        except ZeroDivisionError:
            return 0.0

    def __eq__(self, other):
        if isinstance(other, _TargetSequenceMatchCandidate):
            return self.hits == other.hits and self.misses == other.misses
        return False

    def __gt__(self, other):
        if isinstance(other, _TargetSequenceMatchCandidate):
            return self.hits > other.hits and self.misses < other.misses
        return super(_TargetSequenceMatchCandidate, self).__gt__(other)

    def __lt__(self, other):
        if isinstance(other, _TargetSequenceMatchCandidate):
            return self.hits < other.hits and self.misses > other.misses
        return super(_TargetSequenceMatchCandidate, self).__lt__(other)
