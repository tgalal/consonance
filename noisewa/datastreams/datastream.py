import logging

logger = logging.getLogger(__file__)

class DataStream(object):
    def read(self, readsize):
        """
        :param readsize:
        :type readsize: int
        :return:
        :rtype: bytes
        """

    def write(self, data):
        """
        :param data:
        :type data: bytes
        :return:
        :rtype:
        """
        logger.debug("write: %s" % [d for d in data])
