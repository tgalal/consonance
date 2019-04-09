class PrivateKey(object):
    def __init__(self, data):
        """
        :param data:
        :type data: bytes
        """
        self._data = data  # type: bytes

    @property
    def data(self):
        return self._data

    def __eq__(self, other):
        return type(other) is PrivateKey and self.data == other.data
