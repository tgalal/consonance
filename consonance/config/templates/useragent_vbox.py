from ..useragent import UserAgentConfig
from ..appversion import AppVersionConfig


class VBoxUserAgentConfig(UserAgentConfig):

    DEFAULT_LOCALE_LANG = 'en'
    DEFAULT_LOCALE_COUNTRY = 'US'
    DEFAULT_MCC = '000'
    DEFAULT_MNC = '000'
    OS_VERSION = "5.0"
    OS_BUILD_NUMBER = "vbox86p-userdebug 5.0 LRX21M 233 test-keys"
    MANUFACTURER = "unknown"
    DEVICE = "vbox86p"


    def __init__(self,
                 app_version,
                 phone_id,
                 mcc=None, mnc=None,
                 locale_lang=None,
                 locale_country=None):
        """
        :param app_version:
        :type app_version: str | AppVersion
        """
        if type(app_version) is str:
            app_version = AppVersionConfig(app_version)

        super(VBoxUserAgentConfig, self).__init__(
            platform=0,
            app_version=app_version,
            mcc=mcc or self.DEFAULT_MCC, mnc=mnc or self.DEFAULT_MNC,
            os_version=self.OS_VERSION,
            manufacturer=self.MANUFACTURER,
            device=self.DEVICE,
            os_build_number=self.OS_BUILD_NUMBER,
            phone_id=phone_id,
            locale_lang=locale_lang or self.DEFAULT_LOCALE_LANG,
            locale_country=locale_country or self.DEFAULT_LOCALE_COUNTRY
        )
