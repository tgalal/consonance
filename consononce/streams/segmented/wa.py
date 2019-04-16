import struct

from .segmented import SegmentedStream
from ..arbitrary.arbitrary import ArbitraryStream


class WASegmentedStream(SegmentedStream):
    def __init__(self, dynamicstream):
        """
        :param dynamicstream:
        :type dynamicstream:  DataStream
        """
        self._datastream = dynamicstream # type: ArbitraryStream

    def read_segment(self):
        size = struct.unpack('>I', b"\x00" + self._datastream.read(3))[0] # type: int
        return self._datastream.read(size)

    def write_segment(self, data):
        if len(data) >= 16777216:
            raise ValueError("data too large to write; length=%d" % len(data))

        self._datastream.write(struct.pack('>I', len(data))[1:])
        self._datastream.write(data)
