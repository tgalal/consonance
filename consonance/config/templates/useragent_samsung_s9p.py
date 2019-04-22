from ..useragent import UserAgentConfig


class SamsungS9PUserAgentConfig(UserAgentConfig):
    DEFAULT_LOCALE_LANG = 'en'
    DEFAULT_LOCALE_COUNTRY = 'US'
    DEFAULT_MCC = '000'
    DEFAULT_MNC = '000'
    OS_VERSION = "8.0.0"
    OS_BUILD_NUMBER = "star2ltexx-user 8.0.0 R16NW G965FXXU1ARCC release-keys"
    MANUFACTURER = "samsung"
    DEVICE = "star2lte"

    def __init__(self,
                 app_version,
                 phone_id,
                 mcc=None, mnc=None,
                 locale_lang=None,
                 locale_country=None):
        super(SamsungS9PUserAgentConfig, self).__init__(
            platform=UserAgentConfig.PLATFORM_ANDROID,
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
