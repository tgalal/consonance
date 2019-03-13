from noisewa.models.payload.useragent import UserAgent
from noisewa.models.payload.app_version import AppVersion


class VBoxUserAgent(UserAgent):
    def __init__(self, app_version):
        """
        :param app_version:
        :type app_version: str | AppVersion
        """
        if type(app_version) is str:
            app_version = AppVersion(app_version)

        super(VBoxUserAgent, self).__init__(
            platform=0,
            app_version=app_version,
            mcc="310", mnc="260",
            os_version="5.0",
            manufacturer="unknown",
            device="vbox86p",
            os_build_number="vbox86p-userdebug 5.0 LRX21M 233 test-keys",
            phone_id="f9463e5e-52f8-403d-a4df-d6804529e371",
            locale_lang="en",
            locale_country="US"
        )
