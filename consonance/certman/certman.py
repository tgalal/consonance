from dissononce.dh.x25519.x25519 import PublicKey
from ..proto import wa20_pb2
import axolotl_curve25519 as curve
import logging
import time

logger = logging.getLogger(__name__)


class CertMan(object):
    def __init__(self):
        self._pubkeys = {
            "WhatsAppLongTerm1": bytearray(
                [20, 35, 117, 87, 77, 10, 88, 113, 102, 170, 231, 30, 190, 81, 100, 55, 196, 162, 139,
                 115, 227, 105, 92, 108, 225, 247, 249, 84, 93, 168, 238, 107])
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

        logger.debug(
            "NoiseCertificate(signature=[%d bytes], serial=%d, issuer='%s', expires=%d, subject='%s', ""key=[%d bytes])"
            % (
                len(cert.signature), cert_details.serial, cert_details.issuer, cert_details.expires,
                cert_details.subject, len(cert_details.key)
            )
        )

        if cert_details.issuer not in self._pubkeys:
            logger.error("noise certificate issued by unknown source: issuer=%s" % cert_details.issuer)
            return False

        if curve.verifySignature(bytes(self._pubkeys[cert_details.issuer]), cert.details, cert.signature) != 0:
            logger.error("invalid signature on noise ceritificate; issuer=%s" % cert_details.issuer)
            return False

        if cert_details.key != rs.data:
            logger.error("noise certificate key does not match proposed server static key; issuer=%s" % cert_details.issuer)
            return False

        if cert_details.HasField("expires") and cert_details.expires < int(time.time()):
            logger.error("noise certificate expired; issuer=%s" % cert_details.issuer)
            return False

        return True
