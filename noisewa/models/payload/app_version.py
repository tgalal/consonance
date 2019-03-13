class AppVersion(object):
    def __init__(self, version):
        """
        :param version:
        :type version: str
        """
        dissected = version.split('.')
        assert len(dissected) > 2, "version must be in format x.y.z"
        self._primary, self._secondary, self._tertiary = map(lambda v:int(v), dissected)

    @property
    def primary(self):
        return self._primary

    @property
    def secondary(self):
        return self._secondary

    @property
    def tertiary(self):
        return self._tertiary
