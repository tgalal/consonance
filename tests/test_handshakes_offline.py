from consonance.structs.keypair import KeyPair
from consonance.handshake import WAHandshake
from consonance.config.client import ClientConfig
from consonance.streams.segmented.dummy import DummySegmentedStream
from consonance.config.templates.useragent_vbox import VBoxUserAgentConfig

import uuid
import base64
import unittest


class HandshakesTest(unittest.TestCase):
    KEYPAIR = KeyPair.from_bytes(
        base64.b64decode(b"YJa8Vd9pG0KV2tDYi5V+DMOtSvCEFzRGCzOlGZkvBHzJvBE5C3oC2Fruniw0GBGo7HHgR4TjvjI3C9AihStsVg==")
    )
    PHONE_ID = uuid.uuid4().__str__()
    CONFIG = ClientConfig(
        username=1,
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

    def test_xx_handshake_offline(self):
        stream = DummySegmentedStream([
            base64.b64decode(
                b"GvoBCiCiMwovEL8pYkUdcxCz6w5lvzvyxgAgHiNm4LnOwO8KQxIwt+dvmTcTMcE12jCC"
                b"rbnLcFY+H2/QuKr4/h4BCHy0rDS9rKp63yqRfFX5vEPY0/UGGqMBCfYtpYzsdsU3cN0Bq4ui5Dm0MY/+Yur2cCFb"
                b"tLRgBa858hWFuCIuWKrkE89GrF0uo+wJsolq4miiqMOdXJfuZ2YBZ4paFS2mWjVmQSINRo8J3LzXncUDMeQBO/KkC"
                b"ARw5BTcVkj2gwI6FG+yB/qI8BUJIxxswJc6q+H+HWkNro+Xl6urn5aOwK7bgBSPNctncZGY72NlJByEQCB6Bra7U"
                b"ykzQA==")
        ])
        ephemeral = KeyPair.from_bytes(
            base64.b64decode(
                b"qLt+l8Jh9mUF/QciIRjd7Z0qKyhN//46Xawk5jdL4WF4tFaszfGgyodH3ErvqU5lV4GnOccdy9zj39GU6AAPVQ=="
            )
        )
        # initialize WANoiseProtocol 2.1
        wa_handshake = WAHandshake(2, 1)
        # this should do a XX handshake since we are not passing the remote static public key
        wa_handshake.perform(self.CONFIG, stream, self.KEYPAIR, e=ephemeral)
