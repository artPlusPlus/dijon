class Difference(object):
    @property
    def source_path(self):
        return self._source_path

    @property
    def source_data(self):
        return self._source_data

    @property
    def target_path(self):
        return self._target_path

    @property
    def target_data(self):
        return self._target_data

    def __init__(self, source_path, source_data, target_path, target_data):
        try:
            self._source_path = tuple(source_path)
        except TypeError:
            self._source_path = source_path

        self._source_data = source_data

        try:
            self._target_path = tuple(target_path)
        except TypeError:
            self._target_path = target_path

        self._target_data = target_data
