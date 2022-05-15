class UnSupportVersionError(Exception):
    def __init__(self, versionBytes: bytes, message: str = "UnSupportVersionError"):
        super().__init__(self)
        self.versionBytes = versionBytes
        self.message = message

    def __str__(self):
        return self.message + ": " + str(self.versionBytes)


class VersionNotFoundError(Exception):
    def __init__(self, message: str = "VersionNotFoundError"):
        super().__init__(self)
        self.message = message

    def __str__(self):
        return self.message
