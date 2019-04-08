from dissononce.dh.x25519.x25519 import PublicKey
from noisewa.proto import wa20_pb2
import logging
logger = logging.getLogger(__file__)


class CertMan(object):
    def __init__(self):
        self._certificates = {
            "WhatsAppLongTerm1": ""
        }

    def is_valid(self, rs, certificate_data):
        """
        :param rs:
        :type rs: PublicKey
        :param certificate_data:
        :type certificate_data: bytes
        :return:
        :rtype:
        """
        cert = wa20_pb2.NoiseCertificate()
        cert.ParseFromString(certificate_data)
        cert_details = wa20_pb2.NoiseCertificate.Details()
        cert_details.ParseFromString(cert.details)

        logger.debug("signature=[%d bytes]" % (len(cert.signature)))
        logger.debug("serial=%d" % cert_details.serial)
        logger.debug("issuer=%s" % cert_details.issuer)
        logger.debug("expires=%d" % cert_details.expires)
        logger.debug("subject=%s" % cert_details.subject)
        logger.debug("key=[%d bytes]" % len(cert_details.key))

        return True
