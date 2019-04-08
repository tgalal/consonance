from noisewa.config.client import ClientConfig
from noisewa.handshake import WAHandshake
from noisewa.streams.segmented.segmented import SegmentedStream
from noisewa.transport import WANoiseTransport

from transitions import Machine


class WANoiseProtocol(object):
    STATE_INIT = 'init'
    STATE_HANDSHAKE = 'handshake'
    STATE_TRANSPORT = 'transport'
    STATE_ERROR = 'error'
    STATES = [
        STATE_INIT,
        STATE_HANDSHAKE,
        STATE_TRANSPORT,
        STATE_ERROR
    ]
    TRANSITIONS = [
        ['start', STATE_INIT, STATE_HANDSHAKE],
        ['finish', STATE_HANDSHAKE, STATE_TRANSPORT],
        ['fail', STATE_HANDSHAKE, STATE_ERROR],
        ['fail', STATE_TRANSPORT, STATE_ERROR],
        ['reset', STATE_INIT, '='],
        ['reset', STATE_TRANSPORT, STATE_INIT],
        ['reset', STATE_HANDSHAKE, STATE_INIT],
        ['reset', 'error', STATE_INIT],
        ['send', STATE_TRANSPORT, '='],
        ['receive', STATE_TRANSPORT, '='],
        ['start', STATE_ERROR, STATE_HANDSHAKE]
    ]

    def __init__(self, version_major, version_minor, protocol_state_callbacks=None):
        """
        :param version_major:
        :type version_major: int
        :param version_minor:
        :type version_minor: int
        :param datastream
        :type datastream SegmentedStream
        """
        self._version_major = version_major
        self._version_minor = version_minor
        self._protocol_state_callbacks = protocol_state_callbacks
        self._machine = Machine(
            states=self.STATES, transitions=self.TRANSITIONS, initial='init',
            after_state_change=self._trigger_state_callback
        )  # type: Machine

        self._transport = None # type: WANoiseTransport
        self._last_triggered_state = None

    def _trigger_state_callback(self):
        if self._protocol_state_callbacks is not None and self._last_triggered_state != self._machine.state:
            self._last_triggered_state = self._machine.state
            self._protocol_state_callbacks(self._machine.state)

    @property
    def state(self):
        return self._machine.state

    def start(self, stream, client_config, s, rs=None):
        """
        :param stream
        :type stream: SegmentedStream
        :param client_config:
        :type client_config: ClientConfig
        :return:
        :rtype:
        :param s:
        :type s: noisewa.structs.keypair.KeyPair
        :param rs:
        :type rs: noisewa.structs.publickey.PublicKey
        """
        self._machine.start()
        handshake = WAHandshake(self._version_major, self._version_minor)
        result = handshake.perform(client_config, stream, s, rs)

        if result is not None:
            self._transport = WANoiseTransport(stream, result[0], result[1])
            self._machine.finish()
        else:
            self._machine.fail()

        return result is True

    def reset(self):
        self._machine.reset()
        self._transport = None

    def send(self, data):
        """
        :param data:
        :type data: bytes
        :param datastream
        :type SegmentedDataStream
        :return:
        :rtype:
        """
        self._machine.send()
        self._transport.send(data)

    def receive(self):
        """
        :param datastream
        :type SegmentedDataStream
        :return:
        :rtype: bytes
        """
        self._machine.receive()
        return self._transport.recv()

