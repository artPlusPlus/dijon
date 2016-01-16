class DijonError(Exception):
    pass


class ObjectFieldError(DijonError, KeyError):
    pass


class SequenceItemError(DijonError, IndexError):
    pass