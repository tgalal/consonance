from consonance.structs.keypair import KeyPair
from consonance.protocol import WANoiseProtocol
from consonance.config.client import ClientConfig
from consonance.streams.segmented.wa import WASegmentedStream
from consonance.streams.arbitrary.arbitrary_socket import SocketArbitraryStream
from consonance.config.templates.useragent_samsung_s9p import SamsungS9PUserAgentConfig
import consonance
import uuid
import dissononce
import socket
import logging
import sys
import base64

consonance.logger.setLevel(logging.DEBUG)
dissononce.logger.setLevel(logging.DEBUG)

# username is phone number
USERNAME = 123456789
# on Android fetch client_static_keypair from /data/data/com.whatsapp/shared_prefs/keystore.xml
KEYPAIR = KeyPair.from_bytes(
    base64.b64decode(b"YJa8Vd9pG0KV2tDYi5V+DMOtSvCEFzRGCzOlGZkvBHzJvBE5C3oC2Fruniw0GBGo7HHgR4TjvjI3C9AihStsVg==")
)
# using a random remote public key
WA_PUBLIC = KeyPair.generate().public
# same phone_id/fdid used at registration.
# on Android it's phoneid_id under /data/data/com.whatsapp/shared_prefs/com.whatsapp_preferences.xml
PHONE_ID = uuid.uuid4().__str__()
# create full configuration which will translate later into a protobuf payload
CONFIG = ClientConfig(
    username=USERNAME,
    passive=True,
    useragent=SamsungS9PUserAgentConfig(
        app_version="2.19.51",
        phone_id=PHONE_ID
    ),
    pushname="consonance",
    short_connect=True
)
ENDPOINT = ("e1.whatsapp.net", 443)
HEADER = b"WA\x02\x01"

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(ENDPOINT)
    # send WA header indicating protocol version
    s.send(HEADER)
    # use WASegmentedStream for sending/receiving in frames
    stream = WASegmentedStream(SocketArbitraryStream(s))
    # initialize WANoiseProtocol 2.1
    wa_noiseprotocol = WANoiseProtocol(2, 1)
    # start the protocol, this should attempt a IK handshake since we
    # specifying the remote static public key. The handshake should
    # fail because WA_PUBLIC is invalid. This results in reverting to
    # a xxfallack handshake. Note that eventually authentication
    # should fail anyways due to invalid credentials of this examples.
    if wa_noiseprotocol.start(stream, CONFIG, KEYPAIR, rs=WA_PUBLIC):
        print("Handshake completed, checking authentication...")
        # we are now in transport phase, first incoming data
        # will indicate whether we are authenticated
        first_transport_data = wa_noiseprotocol.receive()
        # fourth byte is status, 172 is success, 52 is failure
        if first_transport_data[3] == 172:
            print("Authentication succeeded")
        elif first_transport_data[3] == 52:
            print("Authentication failed")
            sys.exit(1)
        else:
            print("Unrecognized authentication response: %s" % (first_transport_data[3]))
            sys.exit(1)
    else:
        print("Handshake failed")
        sys.exit(1)
