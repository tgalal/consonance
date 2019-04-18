from dissononce.processing.cipherstate import CipherState
from .streams.segmented.segmented import SegmentedStream


class WANoiseTransport(object):
    def __init__(self, stream, send_cipherstate, recv_cipherstate):
        """
        :param stream:
        :type stream: SegmentedStream
        :param send_cipherstate:
        :type send_cipherstate: CipherState
        :param recv_cipherstate:
        :type recv_cipherstate: CipherState
        """
        self._stream = stream
        self._send_cipherstate = send_cipherstate
        self._recv_cipherstate = recv_cipherstate

    def send(self, plaintext):
        """
        :param plaintext:
        :type plaintext: bytes
        :return:
        :rtype:
        """
        ciphertext = self._send_cipherstate.encrypt_with_ad(b'', plaintext)
        self._stream.write_segment(ciphertext)

    def recv(self):
        """
        :return:
        :rtype: bytes
        """
        ciphertext = self._stream.read_segment()
        plaintext = self._recv_cipherstate.decrypt_with_ad(b'', ciphertext)
        return bytearray(plaintext)
