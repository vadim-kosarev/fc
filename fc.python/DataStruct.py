import base64


# ======================================================================================================================
class DataValidState:
    def __init__(self, **kwargs):
        self._isValid = False

    def isValid(self):
        return self._isValid

    def invalidate(self):
        self._isValid = False

    def ensureValid(self):
        if not self.isValid():
            self.calculate()
        self._isValid = True

    def calculate(self):
        return


# ======================================================================================================================
class MessageFile(DataValidState):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, mime, binary, **kwargs):
        super().__init__(**kwargs)
        self._mime = mime
        self._binary = binary
        self._isValid = False
        self._binaryStr = None
        self.invalidate()

    # ------------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return "Mime: {}, Lenght: {} bytes".format(self._mime, len(self._binary))

    def calculate(self):
        self._binaryStr = base64.b64encode(self._binary).decode("utf-8")

    def getMime(self):
        return self._mime

    def getBinary(self):
        return self._binary

    def setBinary(self, binary):
        self._binary = binary
        self.invalidate()

    def getBinaryStr(self):
        self.ensureValid()
        return self._binaryStr


# ======================================================================================================================
def escapeHeader(strArg):
    if str is None:
        return "UNDEF"
    strArg = str(strArg)
    strArg = strArg.replace(":", "_#_")
    strArg = strArg.replace("..", "_")
    strArg = strArg.replace("\\", "/")
    strArg = strArg.replace("//", "/")
    return strArg

def gets3Path(headers):
    s3Path = "local/jpgdata/{}/{}/{}/frame_{}_{}_{}.jpg".format(
        escapeHeader(headers["hostname"]),
        escapeHeader(headers["source"]),
        escapeHeader(headers["uuid"]),
        escapeHeader(headers["timestamp"]),
        escapeHeader(headers["frameNo"]),
        escapeHeader(headers["localID"])
    )
    return s3Path


# ======================================================================================================================
class Message(DataValidState):

    def __init__(self, headers, file, **kwargs):
        super().__init__(**kwargs)
        self.headers = headers
        self.file = file


    def __repr__(self):
        return self.__str__()


    def __str__(self):
        return "\nHeaders= {}\nfile= {}".format(self.headers, self.file)

    @staticmethod
    def jsonSerialize(obj, **kwargs):
        if isinstance(obj, Message):
            return {
                "file": obj.file
            }
        if isinstance(obj, MessageFile):
            return {
                "mime": obj.getMime(),
                "data": obj.getBinaryStr()
            }
        return None

    def escapeHeader(self, strArg):
        if str is None:
            return "UNDEF"
        strArg = str(strArg)
        strArg = strArg.replace(":", "_#_")
        strArg = strArg.replace("..", "_")
        strArg = strArg.replace("\\", "/")
        strArg = strArg.replace("//", "/")
        return strArg

    def calculate(self):
        s3Path = gets3Path(self.headers)
        self.headers['frameStoragePath'] = s3Path


# ======================================================================================================================

class Pnt:
    def __init__(self, x, y, **kwargs):
        super().__init__(**kwargs)
        self.x = x
        self.y = y


class FaceBox:
    def __init__(self, p1, p2, **kwargs):
        super().__init__(**kwargs)
        self.p1 = p1
        self.p2 = p2


# ----------------------------------------------------------------------------------------------------------------------
class FaceDetection:
    def __init__(self, detection=0.0, faceBox=None, faceVector=None, faceIndex=0, **kwargs):
        super().__init__(**kwargs)
        self.detection = float(detection)
        self.faceBox = faceBox
        self.faceVector = faceVector
        self.faceIndex = faceIndex

    @staticmethod
    def jsonSerialize(obj, **kwargs):
        if isinstance(obj, FaceDetection):
            return {
                "faceIndex": obj.faceIndex,
                "detection": float(obj.detection),
                "faceBox": obj.faceBox,
                "faceVector": obj.faceVector
            }
        if isinstance(obj, FaceBox):
            return {
                "p1": obj.p1,
                "p2": obj.p2
            }
        if isinstance(obj, Pnt):
            return {
                "x": obj.x,
                "y": obj.y
            }
        return None
