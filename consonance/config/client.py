from .useragent import UserAgentConfig


class ClientConfig(object):
    STR_TEMPLATE = """ClientConfig(
    username={username},
    passive={passive},
    useragent={useragent},
    pushname={pushname},
    short_connect={short_connect}
)"""

    def __init__(self,
                 username,
                 passive,
                 useragent,
                 pushname,
                 short_connect=True,
                 ):
        """
        :param username:
        :type username: int
        :param passive:
        :type passive: bool
        :param useragent:
        :type useragent: UserAgentConfig
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

    def __str__(self):
        return self.STR_TEMPLATE.format(
            username=self.username,
            passive=self.passive,
            useragent=self.useragent,
            pushname=self.pushname,
            short_connect=self.short_connect
        )

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
