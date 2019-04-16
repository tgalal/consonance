from .segmented import SegmentedStream

try:
    import Queue
except ImportError:
    import queue as Queue


class BlockingQueueSegmentedStream(SegmentedStream):

    EVENT_READ  = 1
    EVENT_WRITE = 2

    def __init__(self):
        self._readqueue = Queue.Queue()
        self._writequeue = Queue.Queue()
        self._events_callback = None

    def set_events_callback(self, events_callback):
        self._events_callback = events_callback

    def remove_events_callback(self):
        self._events_callback = None

    def put_read_segment(self, data):
        """
        :param data:
        :type data: bytes
        :return:
        :rtype:
        """
        self._readqueue.put(data)

    def get_write_segment(self):
        """
        :return:
        :rtype: bytes
        """
        return self._writequeue.get(block=True)

    def read_segment(self):
        if self._events_callback is not None:
            self._events_callback(self.EVENT_READ)

        return self._readqueue.get(block=True)

    def write_segment(self, data):
        self._writequeue.put(data)

        if self._events_callback is not None:
            self._events_callback(self.EVENT_WRITE)

