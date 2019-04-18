from .segmented import SegmentedStream


class DummySegmentedStream(SegmentedStream):
    def __init__(self, data):
        """
        :param data:
        :type data: list[bytes]
        """
        self._read = data  # type: list[bytes]
        self._sent = []  # type: list[bytes]

    def read_segment(self):
        """
        :return:
        :rtype: bytes
        """
        return self._read.pop(0)

    def write_segment(self, data):
        """
        :param data:
        :type data: bytes
        :return:
        :rtype:
        """
        self._sent.append(data)
