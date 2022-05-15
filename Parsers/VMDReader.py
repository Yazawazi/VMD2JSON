import struct

from Log import Log
from Utils.MainDecode import MainDecode
from Utils.StaticBytes import StaticBytes
from Utils.FloatHelper import FloatHelper
from Exceptions.ParserErrors import UnSupportVersionError, VersionNotFoundError


class VMDReader:
    def __init__(self, filePath: str) -> None:
        self.filePath = filePath
        self.fileBytes = open(self.filePath, "rb").read()
        self.currentPosition = 0
        self.staticBytes = StaticBytes()

    def readBytes(self, length: int) -> bytes:
        self.currentPosition += length
        return self.fileBytes[self.currentPosition - length:self.currentPosition]

    def skipBytes(self, length: int) -> None:
        self.currentPosition += length

    def readByteSkipByte(self, readLength: int, skipLength: int) -> bytes:
        oneBytes = self.readBytes(readLength)
        self.skipBytes(skipLength)
        return oneBytes

    def readVersion(self) -> int:
        version = self.readBytes(30)
        if version == self.staticBytes.getVersionStaticBytes(1):
            return 1
        elif version == self.staticBytes.getVersionStaticBytes(2):
            return 2
        else:
            raise UnSupportVersionError(version, "Unsupported version number, please check if the file is a VMD file!")

    def readModelName(self, version: int) -> str:
        if version == 1:
            modelName = self.readBytes(10)
        elif version == 2:
            modelName = self.readBytes(20)
        else:
            raise VersionNotFoundError("Failed to read model name, version number not found.")
        return MainDecode.bytesToShiftJISString(modelName)

    def readBoneKeyFrameNumber(self) -> int:
        return int.from_bytes(self.readBytes(4), byteorder = "little", signed = False)

    def readMorphKeyFrameNumber(self) -> int:
        return int.from_bytes(self.readBytes(4), byteorder = "little", signed = False)

    def readCameraKeyFrameNumber(self) -> int:
        return int.from_bytes(self.readBytes(4), byteorder = "little", signed = False)

    def readLightKeyFrameNumber(self) -> int:
        return int.from_bytes(self.readBytes(4), byteorder = "little", signed = False)

    def readLightKeyFrameRecord(self, lightKeyFrameNumber: int) -> list:
        lightKeyFrameRecord = []
        for i in range(lightKeyFrameNumber):
            lightKeyFrameRecord.append(self.readLightKeyFrameRecordItem())
        return lightKeyFrameRecord

    def readLightKeyFrameRecordItem(self) -> dict:
        lightKeyFrameRecordItem = {
            "FrameTime": int.from_bytes(self.readBytes(4), byteorder = "little", signed = False),
            "LightColor": {
                "R": FloatHelper.bytesToFloat(self.readBytes(4)),
                "G": FloatHelper.bytesToFloat(self.readBytes(4)),
                "B": FloatHelper.bytesToFloat(self.readBytes(4))
            },
            "Direction": {
                "X": FloatHelper.bytesToFloat(self.readBytes(4)),
                "Y": FloatHelper.bytesToFloat(self.readBytes(4)),
                "Z": FloatHelper.bytesToFloat(self.readBytes(4))
            }
        }
        return lightKeyFrameRecordItem

    def readCameraKeyFrameRecord(self, cameraKeyFrameNumber: int) -> list:
        cameraKeyFrameRecord = []
        for i in range(cameraKeyFrameNumber):
            cameraKeyFrameRecord.append(self.readCameraKeyFrameRecordItem())
        return cameraKeyFrameRecord

    def readCameraKeyFrameRecordItem(self) -> dict:
        cameraKeyFrameRecordItem = {
            "FrameTime": int.from_bytes(self.readBytes(4), byteorder = "little", signed = False),
            "Distance": FloatHelper.bytesToFloat(self.readBytes(4)),
            "Position": {
                "X": FloatHelper.bytesToFloat(self.readBytes(4)),
                "Y": FloatHelper.bytesToFloat(self.readBytes(4)),
                "Z": FloatHelper.bytesToFloat(self.readBytes(4))
            },
            "Rotation": {
                "X": FloatHelper.bytesToFloat(self.readBytes(4)),
                "Y": FloatHelper.bytesToFloat(self.readBytes(4)),
                "Z": FloatHelper.bytesToFloat(self.readBytes(4))
            },
            "Curve": struct.unpack("!24s", self.readBytes(24))[0],
            "ViewAngle": int.from_bytes(self.readBytes(4), byteorder = "little", signed = False),
            "Orthographic": int.from_bytes(self.readBytes(1), byteorder = "little", signed = False),
        }
        return cameraKeyFrameRecordItem

    def readMorphKeyFrameRecord(self, morphKeyFrameNumber: int) -> list:
        morphKeyFrameRecord = []
        for i in range(morphKeyFrameNumber):
            morphKeyFrameRecord.append(self.readMorphKeyFrameRecordItem())
        return morphKeyFrameRecord

    def readMorphKeyFrameRecordItem(self) -> dict:
        morphKeyFrameRecordItem = {
            "MorphName": MainDecode.bytesToShiftJISString(self.readBytes(15)),
            "FrameTime": int.from_bytes(self.readBytes(4), byteorder = "little", signed = False),
            "Weight": FloatHelper.bytesToFloat(self.readBytes(4))
        }
        return morphKeyFrameRecordItem

    def readBoneKeyFrameRecord(self, boneKeyFrameNumber: int) -> list:
        boneKeyFrameRecord = []
        for i in range(boneKeyFrameNumber):
            boneKeyFrameRecord.append(self.readBoneKeyFrameRecordItem())
        return boneKeyFrameRecord

    def readBoneKeyFrameRecordItem(self) -> dict:
        boneKeyFrameRecordItem = {
            "BoneName": MainDecode.bytesToShiftJISString(self.readBytes(15)),
            "FrameTime": int.from_bytes(self.readBytes(4), byteorder = "little", signed = False),
            "Position": {
                "X": FloatHelper.bytesToFloat(self.readBytes(4)),
                "Y": FloatHelper.bytesToFloat(self.readBytes(4)),
                "Z": FloatHelper.bytesToFloat(self.readBytes(4))
            },
            "Rotation": {
                "X": FloatHelper.bytesToFloat(self.readBytes(4)),
                "Y": FloatHelper.bytesToFloat(self.readBytes(4)),
                "Z": FloatHelper.bytesToFloat(self.readBytes(4)),
                "W": FloatHelper.bytesToFloat(self.readBytes(4)),
            },
            "Curve": {
                "X": [
                    int.from_bytes(self.readByteSkipByte(1, 3), byteorder = "little", signed = False),
                    int.from_bytes(self.readByteSkipByte(1, 3), byteorder = "little", signed = False),
                    int.from_bytes(self.readByteSkipByte(1, 3), byteorder = "little", signed = False),
                    int.from_bytes(self.readByteSkipByte(1, 3), byteorder = "little", signed = False)
                ],
                "Y": [
                    int.from_bytes(self.readByteSkipByte(1, 3), byteorder = "little", signed = False),
                    int.from_bytes(self.readByteSkipByte(1, 3), byteorder = "little", signed = False),
                    int.from_bytes(self.readByteSkipByte(1, 3), byteorder = "little", signed = False),
                    int.from_bytes(self.readByteSkipByte(1, 3), byteorder = "little", signed = False)
                ],
                "Z": [
                    int.from_bytes(self.readByteSkipByte(1, 3), byteorder = "little", signed = False),
                    int.from_bytes(self.readByteSkipByte(1, 3), byteorder = "little", signed = False),
                    int.from_bytes(self.readByteSkipByte(1, 3), byteorder = "little", signed = False),
                    int.from_bytes(self.readByteSkipByte(1, 3), byteorder = "little", signed = False)
                ],
                "Rotation": [
                    int.from_bytes(self.readByteSkipByte(1, 3), byteorder = "little", signed = False),
                    int.from_bytes(self.readByteSkipByte(1, 3), byteorder = "little", signed = False),
                    int.from_bytes(self.readByteSkipByte(1, 3), byteorder = "little", signed = False),
                    int.from_bytes(self.readByteSkipByte(1, 3), byteorder = "little", signed = False)
                ]
            }
        }
        return boneKeyFrameRecordItem

    def read(self) -> dict:
        Log.log("info", "Reading VMD file...")
        Log.log("info", "Reading version...")
        version = self.readVersion()
        Log.log("info", "Reading model name...")
        modelName = self.readModelName(version)
        Log.log("info", "Reading bone key frame records...")
        boneKeyFrameNumber = self.readBoneKeyFrameNumber()
        boneKeyFrameRecord = self.readBoneKeyFrameRecord(boneKeyFrameNumber)
        Log.log("info", "Reading morph key frame records...")
        morphKeyFrameNumber = self.readMorphKeyFrameNumber()
        morphKeyFrameRecord = self.readMorphKeyFrameRecord(morphKeyFrameNumber)
        Log.log("info", "Reading camera key frame records...")
        cameraKeyFrameNumber = self.readCameraKeyFrameNumber()
        cameraKeyFrameRecord = self.readCameraKeyFrameRecord(cameraKeyFrameNumber)
        Log.log("info", "Reading light key frame records...")
        lightKeyFrameNumber = self.readLightKeyFrameNumber()
        lightKeyFrameRecord = self.readLightKeyFrameRecord(lightKeyFrameNumber)
        Log.log("info", "Done!")
        return {
            "BasicInfo": {
                "Version": version,
                "ModelName": modelName
            },
            "BoneKeyFrame": {
                "Number": boneKeyFrameNumber,
                "Record": boneKeyFrameRecord
            },
            "MorphKeyFrame": {
                "Number": morphKeyFrameNumber,
                "Record": morphKeyFrameRecord
            },
            "CameraKeyFrame": {
                "Number": cameraKeyFrameNumber,
                "Record": cameraKeyFrameRecord
            },
            "LightKeyFrame": {
                "Number": lightKeyFrameNumber,
                "Record": lightKeyFrameRecord
            }
        }
