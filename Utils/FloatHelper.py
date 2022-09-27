import struct


class FloatHelper:
    def __init__(self) -> None:
        pass

    @staticmethod
    def bytesToFloat(byteArray):
        result = struct.unpack("<f", byteArray)[0]
        if result == float("NaN"):
            result = 0.0
        return result
