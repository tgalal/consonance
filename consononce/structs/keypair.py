from .publickey import PublicKey
from .privatekey import PrivateKey

from dissononce.dh.x25519.x25519 import X25519DH
from dissononce.dh.x25519.keypair import KeyPair as X25519KeyPair


class KeyPair(object):
    def __init__(self, public, private):
        """
        :param public:
        :type public: PublicKey
        :param private:
        :type private: PrivateKey
        """
        self._public = public  # type: PublicKey
        self._private = private  # type: PrivateKey
        
    @property
    def public(self):
        return self._public

    @property
    def private(self):
        return self._private

    def __eq__(self, other):
        return type(other) is KeyPair and other.public == self.public and other.private == self.private

    @classmethod
    def generate(cls):
        """
        :return:
        :rtype: KeyPair
        """
        keypair = X25519DH().generate_keypair()
        return KeyPair(
            PublicKey(
                keypair.public.data
            ),
            PrivateKey(
                keypair.private.data
            )
        )

    @classmethod
    def from_bytes(cls, data):
        """
        :param data:
        :type data: bytes
        :return:
        :rtype: KeyPair
        """
        keypair = X25519KeyPair.from_bytes(data)
        return KeyPair(
            PublicKey(
                keypair.public.data
            ),
            PrivateKey(
                keypair.private.data
            )
        )

