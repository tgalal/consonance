from .appversion import AppVersionConfig


class UserAgentConfig(object):
    PLATFORM_ANDROID = 0
    PLATFORM_IOS = 1
    PLATFORM_WINDOWS_PHONE = 2
    PLATFORM_PYTHON_CLIENT = 7

    STR_TEMPLATE = """UserAgentConfig(
        platform={platform},
        app_version={app_version},
        mcc={mcc},
        mnc={mnc},
        os_version={os_version},
        manufacturer={manufacturer},
        device={device},
        os_build_number={os_build_number},
        phone_id={phone_id},
        locale_lang={locale_lang},
        locale_country={locale_country}
    )"""

    def __init__(self,
                 platform,
                 app_version,
                 mcc, mnc,
                 os_version, manufacturer, device, os_build_number,
                 phone_id,
                 locale_lang,
                 locale_country
                 ):
        """
        :param platform:
        :type platform: int
        :param app_version:
        :type app_version: AppVersionConfig | str
        :param mcc:
        :type mcc: str
        :param mnc:
        :type mnc: str
        :param os_version:
        :type os_version: str
        :param manufacturer:
        :type manufacturer: str
        :param device:
        :type device: str
        :param os_build_number:
        :type os_build_number:
        :param phone_id:
        :type phone_id:
        :param locale_lang:
        :type locale_lang: str
        :param locale_country:
        :type locale_country: str
        """
        if type(app_version) is str:
            app_version = AppVersionConfig(app_version)
        self._platform = platform
        self._app_version = app_version
        self._mcc = mcc
        self._mnc = mnc
        self._os_version = os_version
        self._manufacturer = manufacturer
        self._device = device
        self._os_build_number = os_build_number
        self._phone_id = phone_id
        self._locale_lang = locale_lang
        self._locale_country = locale_country

    def __str__(self):
        return self.STR_TEMPLATE.format(
            platform=self.platform,
            app_version=self.app_version,
            mcc=self.mcc,
            mnc=self.mnc,
            os_version=self.os_version,
            manufacturer=self.manufacturer,
            device=self.device,
            os_build_number=self.os_build_number,
            phone_id=self.phone_id,
            locale_lang=self.locale_lang,
            locale_country=self.locale_country
        )

    @property
    def platform(self):
        return self._platform

    @property
    def app_version(self):
        return self._app_version
    @property
    def mcc(self):
        return self._mcc

    @property
    def mnc(self):
        return self._mnc

    @property
    def os_version(self):
        return self._os_version

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def device(self):
        return self._device

    @property
    def os_build_number(self):
        return self._os_build_number

    @property
    def phone_id(self):
        return self._phone_id

    @property
    def locale_lang(self):
        return self._locale_lang

    @property
    def locale_country(self):
        return self._locale_country
