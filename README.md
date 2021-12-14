# Consonance

Consonance implements WhatsApp's handshake process which makes use of Noise Pipes with Curve25519, AES-GCM,
and SHA256 from Noise Protocol.

## META-INF
```
consonance version: 0.1.5
released: 2021-12-14
requires:
- python>=2.5,<=3.7
- dissononce >= 0.34.3
- transitions
- protobuf >= 3.6.0
- python-axolotl-curve25519
```

## Installation

From source:
```
python setup.py install
```
Using Pip:
```
pip install consonance
```

## Usage

### Configuration

Before performing a handshake, you have to define your configuration as a WhatsApp client. This can be done by passing
the configuration parameters to an instance of ```ClientConfig```. Normally this configuration includes details about
the device WhatsApp is running on. Those device details are to be passed to ClientConfig's ```useragent``` parameters
through an instance of ```consonance.config.useragent.UserAgentConfig```. In order to facilitate usage, 
templates for ```UserAgentConfig``` with some pre-set parameters exist under ```consonance/config/templates```. 

```python
from consonance.config.client import ClientConfig
from consonance.config.templates.useragent_samsung_s9p import SamsungS9PUserAgentConfig
import uuid

client_config = ClientConfig(
    username=999999999,  # username/phone number
    passive=True,  # passive connection, you will not send any data after handshake, only receive
    useragent=SamsungS9PUserAgentConfig(
        app_version="2.19.51",  # WhatsApp app version to pose as
        phone_id=str(uuid.uuid4())  # uuid that was used to register the aforementioned username
    ),
    pushname="consonance"  # display name for push notifications
)
```

In addition to ```ClientConfig``` one must possess a KeyPair that'll be used in the handshake process and for
authenticating yourself to WhatsApp. This KeyPair was produced and used during registration and therefore the 
same one has to be used here for a successful authentication. For testing purposes you could always generate a
fresh KeyPair, in which case the handshake process would go through but authentication fails.

```python
from consonance.structs.keypair import KeyPair
import base64

keypair = KeyPair.generate()
# or keypair used at registration, deserialized from concat. of private_bytes and public_bytes
keypair = KeyPair.from_bytes(
    base64.b64decode(b"YJa8Vd9pG0KV2tDYi5V+DMOtSvCEFzRGCzOlGZkvBHzJvBE5C3oC2Fruniw0GBGo7HHgR4TjvjI3C9AihStsVg==")
)
```

### Connect and Authenticate

With your ```ClientConfig``` and ```KeyPair``` you can now attempt a login to WhatsApp. The example below will
demonstrate a [XX](https://noiseprotocol.org/noise.html#interactive-handshake-patterns-fundamental) handshake since
we are not specifying WhatsApp's static public key:

```python
from consonance.protocol import WANoiseProtocol
from consonance.streams.segmented.wa import WASegmentedStream
from consonance.streams.arbitrary.arbitrary_socket import SocketArbitraryStream
import socket


wa_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wa_socket.connect(("e1.whatsapp.net", 443))
# send WA header indicating protocol version
wa_socket.send(b"WA\x04\x00")
# use WASegmentedStream for sending/receiving in frames
wa_socket_stream = WASegmentedStream(SocketArbitraryStream(wa_socket))
# initialize WANoiseProtocol
wa_noiseprotocol = WANoiseProtocol(4, 0)
# start the protocol, this should perform a XX handshake since
# we are not passing the remote static public key
try:
    wa_noiseprotocol.start(wa_socket_stream, client_config, keypair)
    print("Handshake completed, checking authentication...")
    # we are now in transport phase, first incoming data
    # will indicate whether we are authenticated
    first_transport_data = wa_noiseprotocol.receive()
    assert first_transport_data == 51
except:
    print("Handshake failed")
```

- See [examples/walogin_handshake_xx.py](examples/walogin_handshake_xx.py) for the full ```XX``` handshake example.
- See [examples/walogin_handshake_ik.py](examples/walogin_handshake_ik.py) for a ```IK``` handshake example.
- See [examples/walogin_handshake_xxfallback.py](examples/walogin_handshake_xxfallback.py) for a ```XXfallback```
 handshake example.
- See [Interactive handshake patterns](https://noiseprotocol.org/noise.html#interactive-handshake-patterns-fundamental)
and [Noise Pipes](https://noiseprotocol.org/noise.html#noise-pipes) from Noise for information about the handshake
types used here.
