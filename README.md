# Consonance

Consonance implements WhatsApp's handshake process which makes use of Noise Pipes with Curve25519, AES-GCM,
and SHA256 from Noise Protocol.

## META-INF
```
consonance version: 0.34.2
released: 2019-xx-xx
requires:
- python>=2.5,<=3.7
- dissononce >= 0.34.2
- transitions
- protobuf
- python-axolotl-curve25519
```

## Installation

From source:
```
python setup.py install
```
Using Pip:
```
pip install dissononce
```

## Usage

### Configuration

Before performing a handshake, you have to define your configuration as a WhatsApp client. This can be done by passing
the configuration parameters to an instance of ```ClientConfig```. Normally this configuration includes details about the 
device WhatsApp is running on. Those device details are to be passed to ClientConfig's ```useragent``` parameters as 
through an instance of ```consonance.config.useragent.UserAgentConfig```. In order to facilitate usage, 
templates for ```UserAgentConfig``` with some pre-set parameters exist under ```consonance/config/templates```. 

```python
from consonance.config.client import ClientConfig
from consonance.config.templates.useragent_vbox import VBoxUserAgentConfig
import uuid

client_config = ClientConfig(
    username=999999999,  # username/phone number
    passive=True,  # passive connection, you will not send any data after handshake, only receive
    useragent=VBoxUserAgentConfig(
        app_version="2.19.51",  # WhatsApp app version to pose as
        phone_id=str(uuid.uuid4())  # uuid that was used to register the aforementioned username
    ),
    pushname="consonance"  # display name for push notifications
)
```

In addition to ```ClientConfig``` one must possess a KeyPair that'll be used in the handshake process and for
authenticating yourself to WhatsApp. This KeyPair was produced and used during registration and therefore the 
same one has to be used at login for a successful authentication. For testing purposes you could always use a 
fresh KeyPair, in which case the handshake process goes through but authentication fails.

```python
from consonance.structs.keypair import KeyPair
import base64

keypair = KeyPair.generate()
# or
keypair = KeyPair.from_bytes(
    base64.b64decode(b"YJa8Vd9pG0KV2tDYi5V+DMOtSvCEFzRGCzOlGZkvBHzJvBE5C3oC2Fruniw0GBGo7HHgR4TjvjI3C9AihStsVg==")
)
```

### Connect and Authenticate

```python
from consonance.protocol import WANoiseProtocol
from consonance.streams.segmented.wa import WASegmentedStream
from consonance.streams.arbitrary.arbitrary_socket import SocketArbitraryStream
import socket
wa_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wa_socket.connect(("e1.whatsapp.net", 443))
# send WA header indicating protocol version
wa_socket.send(b"WA\x02\x01")
# use WASegmentedStream for sending/receiving in frames
wa_socket_stream = WASegmentedStream(SocketArbitraryStream(wa_socket))
# initialize WANoiseProtocol 2.1
wa_noiseprotocol = WANoiseProtocol(2, 1)
# start the protocol, this should a XX handshake since
# we are not passing the remote static public key
if wa_noiseprotocol.start(wa_socket_stream, client_config, KEYPAIR):
    print("Handshake completed, checking authentication...")
    # we are now in transport phase, first incoming data
    # will indicate whether we are authenticated
    first_transport_data = wa_noiseprotocol.receive()
```

