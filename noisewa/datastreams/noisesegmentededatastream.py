import struct

from noisewa.datastreams.datastream import DataStream
from noisewa.datastreams.segmenteddatastream import SegmentedDataStream


class NoiseSegmentedDataStream(SegmentedDataStream):
    def __init__(self, datastream):
        """
        :param datastream:
        :type datastream:  DataStream
        """
        self._datastream = datastream # type: DataStream

    def read(self):
        size = struct.unpack('>I', b"\x00" + self._datastream.read(3))[0] # type: int
        return self._datastream.read(size)

    def write(self, data):
        if len(data) >= 16777216:
            raise ValueError("data too large to write; length=%d" % len(data))

        self._datastream.write(struct.pack('>I', len(data))[1:])
        self._datastream.write(data)
