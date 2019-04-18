from consonance.structs.keypair import KeyPair
from consonance.protocol import WANoiseProtocol
from consonance.config.client import ClientConfig
from consonance.streams.segmented.wa import WASegmentedStream
from consonance.streams.arbitrary.arbitrary_socket import SocketArbitraryStream
from consonance.config.templates.useragent_vbox import VBoxUserAgentConfig
import uuid
import socket
import unittest


class HandshakesTest(unittest.TestCase):
    USERNAME = 123456789
    KEYPAIR = KeyPair.generate()
    PHONE_ID = uuid.uuid4().__str__()
    CONFIG = ClientConfig(
        username=USERNAME,
        passive=True,
        useragent=VBoxUserAgentConfig(
            app_version="2.19.51",
            phone_id=PHONE_ID,
            mcc="000",
            mnc="000",
        ),
        pushname="consonance",
        short_connect=True
    )
    ENDPOINT = ("e1.whatsapp.net", 443)
    HEADER = b"WA\x02\x01"

    def test_xx_handshake(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.ENDPOINT)
        # send WA header indicating protocol version
        s.send(self.HEADER)
        # use WASegmentedStream for sending/receiving in frames
        stream = WASegmentedStream(SocketArbitraryStream(s))
        # initialize WANoiseProtocol 2.1
        wa_noiseprotocol = WANoiseProtocol(2, 1)
        # start the protocol, this should a XX handshake since
        # we are not passing the remote static public key
        self.assertTrue(wa_noiseprotocol.start(stream, self.CONFIG, self.KEYPAIR))
        # we are now in transport phase, first incoming data
        # will indicate whether we are authenticated
        first_transport_data = wa_noiseprotocol.receive()
        # fourth byte is status, 172 is success, 52 is failure
        self.assertEqual(52, first_transport_data[3])
