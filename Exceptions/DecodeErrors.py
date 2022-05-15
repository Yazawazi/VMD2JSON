class ShiftJISDecodeError(Exception):
    def __init__(self, message: str = "ShiftJISDecodeError"):
        super().__init__(self)
        self.message = message

    def __str__(self):
        return self.message


class GB2312DecodeError(Exception):
    def __init__(self, message: str = "GB2312DecodeError"):
        super().__init__(self)
        self.message = message

    def __str__(self):
        return self.message
