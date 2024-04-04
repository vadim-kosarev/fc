import argparse
import enum
import logging.config

import cv2

# ------------------------------------------------------------------------------------------------
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)
logger.info("Initialized")

# ------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(
    description='processes faces image')
parser.add_argument(
    "--file",
    type=str,
    default="out/input.jpg",
    help="source file")
parser.add_argument(
    "--prototxt",
    type=str,
    default="github.com/gopinath-balu/computer_vision/CAFFE_DNN/deploy.prototxt.txt",
    help="deploy.prototxt.txt")
parser.add_argument(
    "--caffeModel",
    type=str,
    default="github.com/gopinath-balu/computer_vision/CAFFE_DNN/res10_300x300_ssd_iter_140000.caffemodel",
    help="res10_300x300_ssd_iter_140000.caffemodel")
args = parser.parse_args()


# ------------------------------------------------------------------------------------------------

class ProcResult(enum.Enum):
    OK = 0
    ERROR = -1
    OUT_OF_BOUNDS = -2


def check01(fArr):
    for f in fArr:
        if (f < 0 or f > 1):
            return ProcResult.OUT_OF_BOUNDS
    return ProcResult.OK


class FacesImageProcessor:
    _faceDetector = None

    def __init__(self, prototxt=args.prototxt, caffeModel=args.caffeModel, **kwargs):
        self._faceDetector = cv2.dnn.readNetFromCaffe(prototxt, caffeModel)

    def processBlob(self, blob, shape):
        # (a1, a2, imageHeight, imageWidth) = shape
        (imageHeight, imageWidth, colorBytes) = shape
        faceBoxes = []

        self._faceDetector.setInput(blob)
        detections = self._faceDetector.forward()

        detCount = detections.shape[2]

        for i in range(0, detCount):
            detection = detections[0, 0, i, 2]
            if (detection > 0.5):
                if (check01([
                    detections[0, 0, i, 3], detections[0, 0, i, 4],
                    detections[0, 0, i, 5], detections[0, 0, i, 6]
                ]) != ProcResult.OK):
                    logger.info("OUT_OF_BOUNDS... %d", i)
                else:
                    x1 = int(detections[0, 0, i, 3] * imageWidth)
                    y1 = int(detections[0, 0, i, 4] * imageHeight)
                    x2 = int(detections[0, 0, i, 5] * imageWidth)
                    y2 = int(detections[0, 0, i, 6] * imageHeight)
                    # logger.info("bbox: (%d,%d) - (%d,%d))", x1, y1, x2, y2)
                    faceBoxes.append(((x1, y1), (x2, y2)))
            else:
                break

        return (ProcResult.OK, faceBoxes)

    def processImage(self, image):

        faceBoxes1 = []
        faceBoxes2 = []

        blob1 = cv2.dnn.blobFromImage(
            image
        )

        # blob2 = cv2.dnn.blobFromImage(
        #     image
        #     , scalefactor=1.
        #     , size=(300, 300)
        #     , mean=[104, 117, 123],
        #     swapRB=False, crop=False
        # )

        (res1, faceBoxes1) = self.processBlob(blob1, image.shape)
        # (res2, faceBoxes2) = self.processBlob(blob2, image.shape)

        return faceBoxes1 + faceBoxes2

# ------------------------------------------------------------------------------------------------
if (__name__ == "__main__"):
    logger.info("Started")
    faceImageProcessor = FacesImageProcessor()

    logger.info("Processing %s", args.file)
    image = cv2.imread(args.file)

    (imageHeight, imageWidth, colorDepth) = image.shape
    logger.info("Image: %d x %d", imageWidth, imageHeight)

    faceBoxes = faceImageProcessor.processImage(image)
    logger.info("Detection count: %d", len(faceBoxes))

    for faceBox in faceBoxes:
        (x1, y1), (x2, y2) = faceBox
        logger.info("bbox: (%d,%d) - (%d,%d))", x1, y1, x2, y2)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imwrite(args.file + ".dnn.jpeg", image)

    # ------------------------------------------------------------------------------------------------------------------
if (__name__ == "__main0__"):

    logger.info("Started")
    obj = FacesImageProcessor()

    face_detector = cv2.dnn.readNetFromCaffe(args.prototxt, args.caffeModel)

    logger.info("Processing %s", args.file)
    image = cv2.imread(args.file)
    (imageHeight, imageWidth, colorBytes) = image.shape
    logger.info("Image: %d x %d", imageWidth, imageHeight)
    blob = cv2.dnn.blobFromImage(
        image
        ,scalefactor=1.
        ,size=(300,300)
        ,mean=[104, 117, 123],
        swapRB=False, crop=False
    )

    face_detector.setInput(blob)
    detections = face_detector.forward()

    detCount = detections.shape[2]
    logger.info("Detection count: %d", detCount)

    for i in range(0, detCount):
        detection = detections[0, 0, i, 2]
        min = detections.min
        max = detections.max
        if (detection > 0.5):
            xx1 = detections[0, 0, i, 3]
            yy1 = detections[0, 0, i, 4]
            xx2 = detections[0, 0, i, 5]
            yy2 = detections[0, 0, i, 6]
            x1 = int(xx1 * imageWidth)
            y1 = int(yy1 * imageHeight)
            x2 = int(xx2 * imageWidth)
            y2 = int(yy2 * imageHeight)
            logger.info("bbox: (%d,%d) - (%d,%d))", x1, y1, x2, y2)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imwrite(args.file + ".dnn.jpg", image)
