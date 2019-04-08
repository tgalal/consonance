import logging

logger = logging.getLogger(__file__)


class ArbitraryStream(object):
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
