import logging

from ._graph import Graph
import _nodes


_logger = logging.getLogger(__name__)


def compare(source_data, target_data):
    """
    compare identifies differences between two JSON structures.

    :param source_data: The "left" side of the comparison
    :param target_data: The "right" side of the comparison
    :return: Returns a graph
    """
    _logger.debug('begin compare')

    result = Graph()

    source = Graph()
    source.parse(source_data)

    target = Graph()
    target.parse(target_data)

    source = source
    target = target

    try:
        result.root = _compare_object(source.root, target.root)
    except TypeError:
        result.root = _compare_sequence(source.root, target.root)

    _logger.debug('end compare')
    return result


def _compare_object(source, target):
    result = _nodes.Object(target.path, target.data)
    field_pairs = set()

    for src_field in source:
        try:
            tgt_field = target[src_field.path]
            field_pairs.add((src_field, tgt_field))
        except KeyError:
            result_field = _nodes.ObjectFieldDeletion(src_field)
            result[src_field.path] = result_field

    for tgt_field in target:
        try:
            src_field = source[tgt_field.path]
            field_pairs.add((src_field, tgt_field))
        except KeyError:
            result_field = _nodes.ObjectFieldAddition(tgt_field)
            result[tgt_field.path] = result_field

    for src_field, tgt_field in field_pairs:
        result_field = _nodes.ObjectField(tgt_field.path, tgt_field.data)
        try:
            result_field.value = _compare_object(src_field, tgt_field)
        except TypeError:
            try:
                result_field.value = _compare_sequence(src_field, tgt_field)
            except TypeError:
                if src_field.value == tgt_field.value:
                    result_field.value = tgt_field.value
                else:
                    src_field = src_field.copy()
                    tgt_field = tgt_field.copy()
                    result_field = _nodes.ObjectFieldModification(src_field, tgt_field)
        result[result_field.path] = result_field

    return result


def _compare_sequence(source, target, match_threshold=0.1):
    if isinstance(source, basestring):
        raise TypeError('Unsupported source type: basestring')
    elif isinstance(target, basestring):
        raise TypeError('Unsupported target type: basestring')

    result = _nodes.Sequence(source.path, source.data)

    match_data = _compute_sequence_item_matches(source, target)
    matched_src_indices = []
    matched_tgt_indices = []

    for src_idx, tgt_idx, match_hits, match_misses in match_data:
        src_item = source.items[src_idx]
        tgt_item = target.items[tgt_idx]

        if match_hits / (match_hits + match_misses) < match_threshold:
            result_item = _nodes.SequenceItemDeletion(src_item)
            result.items.append(result_item)

            result_item = _nodes.SequenceItemAddition(tgt_item)
            result.items.append(result_item)
            continue

        # At this point, src_item and tgt_item are considered a match
        if src_item.path == tgt_item.path:
            result_item = _nodes.SequenceItem(tgt_item.path, tgt_item.data)
            result.items.append(result_item)
        else:
            result_item = _nodes.SequenceItemModification(src_item, tgt_item)
            result.items.append(result_item)

        try:
            result_item.value = _compare_object(src_item, tgt_item)
        except TypeError:
            try:
                result_item.value = _compare_sequence(src_item, tgt_item)
            except TypeError:
                if src_item.value == tgt_item.value:
                    result_item = _nodes.SequenceItem(tgt_item.path, tgt_item.data)
                else:
                    msg = ''
                    raise RuntimeError()


def _compare_sequence_old(diffs, path, source, target, match_threshold=0.1):
    if isinstance(source, basestring):
        raise TypeError('Unsupported source type: basestring')
    elif isinstance(target, basestring):
        raise TypeError('Unsupported target type: basestring')

    match_data = _compute_sequence_item_matches(source, target)
    matched_src_indices = []
    matched_tgt_indices = []

    for src_idx, tgt_idx, match_hits, match_misses in match_data:
        src_path = path[:]
        src_path.append(src_idx)
        src_item = source[src_idx]

        tgt_path = path[:]
        tgt_path.append(tgt_idx)
        tgt_item = target[tgt_idx]

        if match_hits / (match_hits + match_misses) < match_threshold:
            diff = SequenceItemDeletion(src_path, src_item)
            diffs.append(diff)
            diff = SequenceItemAddition(tgt_path, tgt_item)
            diffs.append(diff)
            continue

        if src_idx != tgt_idx:
            diff = SequenceItemModification(src_path, src_item, tgt_path, tgt_item)
            diffs.append(diff)

        try:
            _compare_object(diffs, src_path, src_item, tgt_item)
        except TypeError:
            try:
                _compare_sequence(diffs, src_path, src_item, tgt_item)
            except TypeError:
                if src_item != tgt_item:
                    # Getting here means the src_item and tgt_item are somewhat equal.
                    # However, they are also neither sequences nor objects.
                    diff = SequenceItemDeletion(src_path, src_item)
                    diffs.append(diff)

                    diff = SequenceItemAddition(tgt_path, tgt_item)
                    diffs.append(diff)

        matched_src_indices.append(src_idx)
        matched_tgt_indices.append(tgt_idx)

    # Identify item deletions
    for src_idx in xrange(0, len(source)):
        if src_idx in matched_src_indices:
            continue

        src_path = path[:]
        src_path.append(src_idx)
        src_item = source[src_idx]

        diff = SequenceItemDeletion(src_path, src_item)
        diffs.append(diff)

    # Identify item additions
    for tgt_idx in xrange(0, len(target)):
        if tgt_idx in matched_tgt_indices:
            continue

        tgt_path = path[:]
        tgt_path.append(tgt_idx)
        tgt_item = target[tgt_idx]

        diff = SequenceItemAddition(tgt_path, tgt_item)
        diffs.append(diff)


def _compute_sequence_item_match_candidates(item, candidates):
    result = []
    for candidate_idx, candidate_value in enumerate(candidates):
        candidate = _TargetSequenceMatchCandidate()
        candidate.target_index = candidate_idx
        candidate.hits, candidate.misses = _compute_value_score(item, candidate_value)
        result.append(candidate)
    result.sort()
    result.reverse()
    # TODO: Handle candidate_indices with same score
    return result


def _compute_sequence_item_matches(source, target):
    result = []

    match_candidates = {}
    for src_idx, src in enumerate(source):
        tgt_candidates = _compute_sequence_item_match_candidates(src, target)
        match_candidates[src_idx] = tgt_candidates

    matches = {}
    rng = len(source) if len(source) < len(target) else len(target)
    while len(matches) < rng and match_candidates:
        round_picks = []
        for src_idx, tgt_candidates in match_candidates.iteritems():
            round_pick = tgt_candidates.pop(0)
            round_picks.append((round_pick.score, src_idx, round_pick))
        round_picks.sort()
        round_picks.reverse()
        for _, src_idx, candidate in round_picks:
            if candidate.target_index in matches:
                continue
            matches[candidate.target_index] = (src_idx, candidate)
            del match_candidates[src_idx]

    for src_idx, match in matches.values():
        result.append((src_idx, match.target_index, match.hits, match.misses))

    return result


def _compute_value_score(source, target):
    """
    Calculates a score representing how closely to values match each other.

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
    Calculates a score representing how closely sequences match each other.

    :param source:
    :param target:
    :return:
    """
    if isinstance(source, basestring):
        raise TypeError('Unsupported source type: basestring')
    elif isinstance(target, basestring):
        raise TypeError('Unsupported target type: basestring')

    hits = 0.0
    misses = abs(len(source)-len(target)) * 2.0

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
        raise TypeError('Unsupported source type: {0}'.format(source.__class__))
    try:
        tgt_keys = target.keys()
    except AttributeError:
        raise TypeError('Unsupported target type: {0}'.format(target.__class__))

    common_keys = set(src_keys).intersection(tgt_keys)
    missing_source_keys = set(tgt_keys).difference(src_keys)
    missing_target_keys = set(src_keys).difference(tgt_keys)

    misses += len(missing_source_keys) * 2
    misses += len(missing_target_keys) * 2

    for key in common_keys:
        hits += 1

        value_hits, value_misses = _compute_value_score(source[key], target[key])
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
