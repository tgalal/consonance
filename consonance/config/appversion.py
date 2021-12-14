class AppVersionConfig(object):
    STR_TEMPLATE = """AppVersionConfig(
            primary={primary},
            secondary={secondary},
            tertiary={tertiary},
            quaternary={quaternary}
        )"""

    def __init__(self, version):
        """
        :param version:
        :type version: str
        """
        dissected = version.split('.')
        padded = dissected + ['0'] * (4 - len(dissected))
        assert len(padded) == 4, "%s is not a valid version" % version

        self._primary, self._secondary, self._tertiary, self._quaternary = map(lambda v:int(v), padded)

    def __str__(self):
        return self.STR_TEMPLATE.format(
            primary=self.primary,
            secondary=self.secondary,
            tertiary=self.tertiary,
            quaternary=self.quaternary
        )

    @property
    def primary(self):
        return self._primary

    @property
    def secondary(self):
        return self._secondary

    @property
    def tertiary(self):
        return self._tertiary

    @property
    def quaternary(self):
        return self._quaternary
