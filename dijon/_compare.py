from ._differences import (ObjectFieldAddition,
                           ObjectFieldDeletion,
                           ObjectFieldModification)
from ._differences import (SequenceItemAddition,
                           SequenceItemDeletion,
                           SequenceItemModification)


def compare(source, target):
    """
    compare identifies differences between two JSON structures.

    :param source: The "left" side of the comparison
    :param target: The "right" side of the comparison
    :return: Returns a list of ```Difference``` instances.
    """
    differences = []
    source = source
    target = target

    try:
        _compare_object(differences, ['root'], source, target)
    except TypeError:
        _compare_sequence(differences, ['root'], source, target)

    return differences


def _compare_object(diffs, path, source, target):
    for field in source:
        src_path = path[:]
        src_path.append(field)
        src_value = source[field]

        tgt_path = path[:]
        tgt_path.append(field)

        try:
            tgt_value = target[field]
            _compare_object(diffs, src_path, src_value, tgt_value)
        except KeyError:
            diff = ObjectFieldDeletion(src_path, src_value)
            diffs.append(diff)
            continue
        except TypeError:
            try:
                _compare_sequence(diffs, src_path, src_value, tgt_value)
            except TypeError:
                if src_value != tgt_value:
                    diff = ObjectFieldModification(src_path, src_value, tgt_path, tgt_value)
                    diffs.append(diff)

    for field in target:
        if field in source:
            continue
        tgt_path = path[:]
        tgt_path.append(field)
        tgt_value = target[field]
        diff = ObjectFieldAddition(tgt_path, tgt_value)
        diffs.append(diff)


def _compare_sequence(diffs, path, source, target, match_threshold=0.1):
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

    rng = len(source) if len(source) < len(target) else len(target)

    match_candidates = {}
    for src_idx, src in enumerate(source):
        tgt_candidates = _compute_sequence_item_match_candidates(src, target)
        match_candidates[src_idx] = tgt_candidates

    matches = {}
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
