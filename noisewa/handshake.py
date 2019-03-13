import random

from dissononce.processing.handshakestate import HandshakeState
from dissononce.processing.handshakepatterns.handshakepattern import HandshakePattern
from dissononce.processing.handshakepatterns.ik import IKHandshakePattern
from dissononce.processing.handshakepatterns.xx import XXHandshakePattern
from dissononce.processing.modifiers.fallback import FallbackPatternModifier
from dissononce.processing.symmetricstate import SymmetricState
from dissononce.processing.cipherstate import CipherState
from dissononce.cipher.aesgcm import AESGCMCipher
from dissononce.hash.sha256 import SHA256Hash
from dissononce.dh.keypair import KeyPair
from dissononce.dh.key_public import PublicKey
from dissononce.dh.x25519DH import X25519DH
from dissononce.util.byte import ByteUtil

from noisewa.models.payload.payload import Payload
from noisewa.proto import wa20_pb2
from noisewa.datastreams.segmenteddatastream import SegmentedDataStream
from noisewa.certman.certman import CertMan

import logging
logger = logging.getLogger(__file__)



class WAHandshake(object):

    PROLOGUE = {
        "2.0": b"WA\x02\x00",
        "2.1": b"WA\x02\x01"
    }

    STATE_INIT = 0
    STATE_WORKING = 1
    STATE_FAILED = 3
    STATE_SUCCEEDED = 4

    def __init__(self, version, payload):
        """
        :param payload:
        :type payload: Payload
        """
        self._payload = payload
        self._handshakestate = HandshakeState(
            SymmetricState(
                CipherState(
                    AESGCMCipher()
                ),
                SHA256Hash()
            ),
            X25519DH() # type: HandshakeState
        )
        self._state = self.STATE_INIT # type: int
        self._cipherstatepair = None # type: tuple[CipherState,CipherState]
        assert version in self.PROLOGUE, "%s is not supported " % version
        self._prologue = self.PROLOGUE[version]

    @property
    def state(self):
        return self._state

    @property
    def cipherstatepair(self):
        return self._cipherstatepair

    @property
    def rs(self):
        return self._handshakestate.rs

    def _create_full_payload(self, payload):
        """
        :param payload:
        :type payload: Payload
        :return:
        :rtype: wa20_pb2.ClientPayload
        """
        client_payload = wa20_pb2.ClientPayload()
        user_agent = wa20_pb2.ClientPayload.UserAgent()
        user_agent_app_version = wa20_pb2.ClientPayload.UserAgent.AppVersion()

        user_agent.platform = payload.useragent.platform
        user_agent.mcc = payload.useragent.mcc
        user_agent.mnc = payload.useragent.mnc
        user_agent.os_version = payload.useragent.os_version
        user_agent.manufacturer = payload.useragent.manufacturer
        user_agent.device = payload.useragent.device
        user_agent.os_build_number = payload.useragent.os_build_number
        user_agent.phone_id = payload.useragent.phone_id
        user_agent.locale_language_iso_639_1 = payload.useragent.locale_lang
        user_agent.locale_country_iso_3166_1_alpha_2 = payload.useragent.locale_country

        user_agent_app_version.primary = payload.useragent.app_version.primary
        user_agent_app_version.secondary = payload.useragent.app_version.secondary
        user_agent_app_version.tertiary = payload.useragent.app_version.tertiary

        user_agent.app_version.MergeFrom(user_agent_app_version)

        client_payload.username = payload.username
        client_payload.passive = payload.passive
        client_payload.push_name = payload.pushname

        max_int = (2**32) / 2

        client_payload.session_id = random.randint(-max_int, max_int-1)
        client_payload.short_connect = payload.short_connect
        client_payload.connect_type = 1
        client_payload.user_agent.MergeFrom(user_agent)

        return client_payload

    def perform(self, datatsream, s, rs=None):
        """
        :param datatsream:
        :type SegmentedDataStream
        :param s:
        :type s: KeyPair
        :param rs:
        :type rs: PublicKey | None
        :return:
        :rtype:
        """
        self._state = self.STATE_WORKING
        if rs is not None:
            self._cipherstatepair = self._perform_ik(datatsream, s, rs)

        self._state = self.STATE_FAILED if self._cipherstatepair is None else self.STATE_SUCCEEDED

        return self._cipherstatepair

    def _perform_fallback(self, handshake_pattern, datastream, s, client_payload, server_hello):
        """
        :param handshake_pattern:
        :type handshake_pattern: HandshakePattern
        :param datastream:
        :type datastream: SegmentedDataStream
        :param s:
        :type s: KeyPair
        :param e:
        :type e: KeyPair
        :param client_payload:
        :type client_payload:
        :param server_hello:
        :type server_hello:
        :return:
        :rtype: tuple(CipherState,CipherState)
        """
        self._handshakestate.modify(
                handshake_pattern=FallbackPatternModifier().modify(handshake_pattern),
                initiator=True,
                prologue=self._prologue,
                s=s
            )
        payload_buffer = bytearray()
        self._handshakestate.read_message(server_hello.ephemeral + server_hello.static + server_hello.payload, payload_buffer)
        certman = CertMan()
        if certman.is_valid(self._handshakestate.rs, bytes(payload_buffer)):
            logger.debug("cert is valid")
        else:
            logger.error("cert is not valid")

        message_buffer = bytearray()

        cipherpair = self._handshakestate.write_message(client_payload.SerializeToString(), message_buffer)

        static, payload = ByteUtil.split(bytes(message_buffer), 48, len(message_buffer) - 48)
        client_finish = wa20_pb2.HandshakeMessage.ClientFinish()
        client_finish.static = static
        client_finish.payload = payload
        outgoing_handshakemessage = wa20_pb2.HandshakeMessage()
        outgoing_handshakemessage.client_finish.MergeFrom(client_finish)
        datastream.write(outgoing_handshakemessage.SerializeToString())

        return cipherpair

    def _perform_ik(self, datastream, s, rs):
        """
        :param datastream:
        :type datastream: SegmentedDataStream
        :param s:
        :type s: KeyPair
        :param rs:
        :type rs: PublicKey
        :return:
        :rtype:
        """
        self._handshakestate.initialize(
            handshake_pattern=IKHandshakePattern(),
            initiator=True,
            prologue=self._prologue,
            s=s,
            rs=rs
        )
        client_payload = self._create_full_payload(self._payload)
        message_buffer = bytearray()
        self._handshakestate.write_message(client_payload.SerializeToString(), message_buffer)
        ephemeral_public, static_public, payload = ByteUtil.split(bytes(message_buffer), 32, 48, len(message_buffer) - 32 + 48)
        handshakemessage = wa20_pb2.HandshakeMessage()
        client_hello = wa20_pb2.HandshakeMessage.ClientHello()

        client_hello.ephemeral = ephemeral_public
        client_hello.static = static_public
        client_hello.payload = payload
        handshakemessage.client_hello.MergeFrom(client_hello)

        datastream.write(handshakemessage.SerializeToString())

        incoming_handshakemessage = wa20_pb2.HandshakeMessage()
        incoming_handshakemessage.ParseFromString(datastream.read())
        if not incoming_handshakemessage.HasField("server_hello"):
            raise ValueError("Handshake message does not contain server hello!")
        server_hello = incoming_handshakemessage.server_hello


        if not server_hello.HasField("static"):
            payload_buffer = bytearray()
            return self._handshakestate.read_message(server_hello.ephemeral + server_hello.static + server_hello.payload, payload_buffer)
        else:
            return self._perform_fallback(XXHandshakePattern(), datastream, s, client_payload, server_hello)
