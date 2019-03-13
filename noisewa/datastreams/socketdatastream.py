from socket import socket

from noisewa.datastreams.datastream import DataStream


class SocketDataStream(DataStream):
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
