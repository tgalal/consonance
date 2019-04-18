from socket import socket

from .arbitrary import ArbitraryStream


class SocketArbitraryStream(ArbitraryStream):
    def __init__(self, socket):
        """
        :param socket:
        :type socket: socket
        """
        self._socket = socket # type: socket

    def read(self, readsize):
        return self._socket.recv(readsize)

    def write(self, data):
        self._socket.send(data)
