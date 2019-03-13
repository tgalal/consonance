from noisewa.models.payload.useragent import UserAgent


class Payload(object):
    def __init__(self,
                 username,
                 passive,
                 useragent,
                 pushname,
                 short_connect,
                 ):
        """
        :param username:
        :type username: int
        :param passive:
        :type passive: bool
        :param useragent:
        :type useragent: UserAgent
        :param pushname:
        :type pushname: str
        :param short_connect:
        :type short_connect: bool
        """
        self._username = username
        self._passive = passive
        self._useragent = useragent
        self._pushname = pushname
        self._short_connect = short_connect

    @property
    def username(self):
        return self._username

    @property
    def passive(self):
        return self._passive

    @property
    def useragent(self):
        return self._useragent

    @property
    def pushname(self):
        return self._pushname

    @property
    def short_connect(self):
        return self._short_connect