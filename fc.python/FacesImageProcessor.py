import argparse
import enum
import json
import logging.config

import cv2

from DataStruct import *

import time
start_time = time.time()
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
    "--suffix",
    type=str,
    default="_dnn.jpeg",
    help="outfile suffix")
parser.add_argument(
    "--debug",
    type=bool,
    default=False,
    help="Dump debug images and info")
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


def adjust01(val):
    if val < 0:
        return 0.
    if val > 1:
        return 1.
    return val


# ----------------------------------------------------------------------------------------------------------------------
class FacesImageProcessor:
    _faceDetector = None
    _prototxt = "github.com/gopinath-balu/computer_vision/CAFFE_DNN/deploy.prototxt.txt"
    _caffemodel = "github.com/gopinath-balu/computer_vision/CAFFE_DNN/res10_300x300_ssd_iter_140000.caffemodel"
    _torch = "github.com/pyannote-data/openface.nn4.small2.v1.t7"

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        self._faceDetector = cv2.dnn.readNetFromCaffe(self._prototxt, self._caffemodel)
        self._embedder = cv2.dnn.readNetFromTorch(self._torch)

    # ------------------------------------------------------------------------------------------------------------------
    def processBlob(self, blob, shape):
        (imageHeight, imageWidth, colorBytes) = shape
        faceBoxes = []

        self._faceDetector.setInput(blob)
        detections = self._faceDetector.forward()

        detCount = detections.shape[2]

        for i in range(0, detCount):
            detection = detections[0, 0, i, 2]
            if (detection > 0.85):
                dToCheck = [
                    detections[0, 0, i, 3], detections[0, 0, i, 4],
                    detections[0, 0, i, 5], detections[0, 0, i, 6]
                ]
                if (check01(dToCheck) != ProcResult.OK):
                    logger.warning("OUT_OF_BOUNDS... %d - %f : %s", i, detection, dToCheck)
                else:
                    x1 = int(adjust01(detections[0, 0, i, 3]) * imageWidth)
                    y1 = int(adjust01(detections[0, 0, i, 4]) * imageHeight)
                    x2 = int(adjust01(detections[0, 0, i, 5]) * imageWidth)
                    y2 = int(adjust01(detections[0, 0, i, 6]) * imageHeight)

                    fd = FaceDetection()
                    fd.detection = detection
                    fd.faceBox = FaceBox(Pnt(x1, y1), Pnt(x2, y2))
                    faceBoxes.append(fd)

            else:
                break

        return (ProcResult.OK, faceBoxes)

    # ------------------------------------------------------------------------------------------------------------------
    def processImage0(self, image):

        faceBoxes1 = []
        faceBoxes2 = []

        blob1 = cv2.dnn.blobFromImage(
            image
        )

        blob2 = cv2.dnn.blobFromImage(
            image
            , scalefactor=1.
            , size=(300, 300)
            , mean=[104, 117, 123],
            swapRB=False, crop=False
        )

        # (res1, faceBoxes1) = self.processBlob(blob1, image.shape)
        (res2, faceBoxes2) = self.processBlob(blob2, image.shape)

        return faceBoxes1 + faceBoxes2

    # ------------------------------------------------------------------------------------------------------------------
    def processImage(self, image, pntShift):
        maxBox = (639, 460)
        (x0, y0) = pntShift

        (imageHeight, imageWidth, colorDepth) = image.shape
        logger.info(f"{args.file}... processing image of size %d x %d", imageWidth, imageHeight)
        faceBoxes = self.processImage0(image)

        # ---- Crop and repeat
        (imgWStep, imgHStep) = (int(imageWidth / 2) + 1, int(imageHeight / 2) + 1)
        if (imageWidth > 2. * maxBox[0]) & (imageHeight > 2. * maxBox[1]):
            for yi in range(0, imageHeight, imgHStep):
                for xi in range(0, imageWidth, imgWStep):

                    (x1, y1) = (xi, yi)
                    (x2, y2) = (xi + imgWStep, yi + imgHStep)
                    crImage = image[y1:y2, x1:x2]
                    fBoxes2 = self.processImage(crImage, (x1, y1))
                    faceBoxes += fBoxes2

                    label = f"CROP_({xi}x{yi})-({x2}x{y2})"
                    logger.info(f"{args.file} {label} : %d faceBoxes", len(fBoxes2))

                    if (args.debug):
                        for fbox2 in fBoxes2:
                            (rx1, ry1) = (fbox2.faceBox.p1.x-xi, fbox2.faceBox.p1.y-yi)
                            (rx2, ry2) = (fbox2.faceBox.p2.x-xi, fbox2.faceBox.p2.y-yi)
                            cv2.rectangle(crImage, (rx1, ry1), (rx2, ry2), (255, 0, 0), 2)
                            logger.info(f"{args.file} Crop file: {label} box: ({rx1}, {ry1}), ({rx2}, {ry2})")

                        cv2.rectangle(crImage, (0, 0), (25, 25), (255, 0, 255), -1)
                        cv2.rectangle(crImage, (0, 0), (imgWStep, imgHStep), (255, 0, 255), 1)
                        cv2.imwrite(f"{args.file}_{label}_{args.suffix}", crImage)

        i = 0
        for r in faceBoxes:
            # 1. calculate 128-D vector
            theFace = image[r.faceBox.p1.y:r.faceBox.p2.y, r.faceBox.p1.x:r.faceBox.p2.x]
            theFaceBlob = cv2.dnn.blobFromImage(theFace, 1./255., (96,96), (0,0,0), swapRB=True, crop=False)
            self._embedder.setInput(theFaceBlob)
            faceVec = self._embedder.forward()

            # logger.info(f"{args.file} faceVec: {faceVec}")
            if (args.debug):
                cv2.imwrite(f"{args.file}_face_{i}_{args.suffix}", theFace)

            # 2. convert faceBox to parent image
            r.faceBox.p1.x += x0
            r.faceBox.p1.y += y0
            r.faceBox.p2.x += x0
            r.faceBox.p2.y += y0

            r.faceVector = faceVec.tolist()[0]

            i += 1
        return faceBoxes


# ------------------------------------------------------------------------------------------------
if (__name__ == "__main__"):
    logger.info("Started")

    faceImageProcessor = FacesImageProcessor()
    logger.info("Processing %s", args.file)
    image = cv2.imread(args.file)

    (imageHeight, imageWidth, colorDepth) = image.shape
    logger.info("Image: %d x %d", imageWidth, imageHeight)

    faceBoxes = faceImageProcessor.processImage(image, (0, 0))
    logger.info("RESULT : Detection count: %d", len(faceBoxes))

    for face in faceBoxes:
        (x1, y1), (x2, y2) = (face.faceBox.p1.x, face.faceBox.p1.y), (face.faceBox.p2.x, face.faceBox.p2.y)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
    cv2.imwrite(f"{args.file}__RRR_{args.suffix}", image)

    sBody = json.dumps(
        faceBoxes,
        ensure_ascii=True,
        default=FaceDetection.jsonSerialize
    )
    logger.info(sBody)

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
        , scalefactor=1.
        , size=(300, 300)
        , mean=[104, 117, 123],
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
            cv2.rectangle(image, (0, 0), (50, 50), (255, 0, 0), 2)

    cv2.imwrite(args.file + ".dnn.jpg", image)

logger.info("%s : Execution time: --- %s seconds ---", args.file, (time.time() - start_time))
