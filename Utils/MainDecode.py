from Exceptions.DecodeErrors import GB2312DecodeError, ShiftJISDecodeError


class MainDecode:
    def __init__(self) -> None:
        pass

    @staticmethod
    def bytesToShiftJISString(byteString: bytes) -> str:
        try:
            eIndex = byteString.index(b"\x00")
        except:
            eIndex = -1
        if eIndex < len(byteString):
            byteString = byteString[:eIndex]
        try:
            return byteString.decode("Shift-JIS")
        except:
            raise ShiftJISDecodeError("Shift-JIS decode error!")

    @staticmethod
    def bytesToGB2312String(byteString: bytes) -> str:
        try:
            eIndex = byteString.index(b"\x00")
        except:
            eIndex = -1
        if eIndex < len(byteString):
            byteString = byteString[:eIndex]
        try:
            return byteString.decode("GB2312")
        except:
            raise GB2312DecodeError("GB2312 decode error!")
