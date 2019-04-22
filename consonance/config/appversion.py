class AppVersionConfig(object):
    STR_TEMPLATE = """AppVersionConfig(
            primary={primary},
            secondary={secondary},
            tertiary={tertiary}
        )"""

    def __init__(self, version):
        """
        :param version:
        :type version: str
        """
        dissected = version.split('.')
        assert len(dissected) > 2, "version must be in format x.y.z"
        self._primary, self._secondary, self._tertiary = map(lambda v:int(v), dissected)

    def __str__(self):
        return self.STR_TEMPLATE.format(
            primary=self.primary,
            secondary=self.secondary,
            tertiary=self.tertiary
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
