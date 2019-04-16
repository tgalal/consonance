from ..proto.wa20_pb2 import HandshakeMessage


class NewRemoteStaticException(Exception):
    def __init__(self, server_hello):
        """
        :param server_hello:
        :type server_hello: HandshakeMessage.ServerHello
        """
        self._server_hello = server_hello # type: HandshakeMessage.ServerHello

    @property
    def server_hello(self):
        return self._server_hello
