from consonance.structs.keypair import KeyPair
from consonance.protocol import WANoiseProtocol
from consonance.config.client import ClientConfig
from consonance.streams.segmented.wa import WASegmentedStream
from consonance.streams.arbitrary.arbitrary_socket import SocketArbitraryStream
from consonance.config.templates.useragent_vbox import VBoxUserAgentConfig
import uuid
import socket
import unittest

PROTOCOL_VERSION = (4, 0)

class HandshakesTest(unittest.TestCase):
    USERNAME = 123456789
    KEYPAIR = KeyPair.generate()
    PHONE_ID = uuid.uuid4().__str__()
    CONFIG = ClientConfig(
        username=USERNAME,
        passive=True,
        useragent=VBoxUserAgentConfig(
            app_version="2.20.206.24",
            phone_id=PHONE_ID,
            mcc="000",
            mnc="000",
        ),
        pushname="consonance",
        short_connect=True
    )
    ENDPOINT = ("e1.whatsapp.net", 443)
    HEADER = b"WA" + bytes(PROTOCOL_VERSION)

    def test_xx_handshake(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.ENDPOINT)
        # send WA header indicating protocol version
        s.send(self.HEADER)
        # use WASegmentedStream for sending/receiving in frames
        stream = WASegmentedStream(SocketArbitraryStream(s))
        # initialize WANoiseProtocol
        wa_noiseprotocol = WANoiseProtocol(*PROTOCOL_VERSION)
        # start the protocol, this should a XX handshake since
        # we are not passing the remote static public key
        wa_noiseprotocol.start(stream, self.CONFIG, self.KEYPAIR)
        # we are now in transport phase, first incoming data
        # will indicate whether we are authenticated
        first_transport_data = wa_noiseprotocol.receive()
        # fourth + fifth byte are status, [237, 38] is failure
        self.assertEqual(b'\xed\x26', first_transport_data[3:5])
