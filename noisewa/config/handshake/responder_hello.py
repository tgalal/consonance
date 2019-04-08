from noisewa.models.payload.payload import Payload


class ResponderHello(object):
    def __init__(self, e, s, payload):
        """
        :param e:
        :type e: bytes
        :param s:
        :type s: bytes
        :param payload:
        :type payload: Payload
        """
        self._e = e
        self._s = s
        self._payload = payload

    @property
    def s(self):
        return self._s

    @property
    def e(self):
        return self._e

    @property
    def payload(self):
        return self._payload
