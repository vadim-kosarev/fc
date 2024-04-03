import argparse
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
class FacesImageProcessor:

    def __init__(self, **kwargs):
        self.jpgBuf = None


# ------------------------------------------------------------------------------------------------
if (__name__ == "__main__"):
    logger.info("Started")
    obj = FacesImageProcessor()

    face_detector = cv2.dnn.readNetFromCaffe(args.prototxt, args.caffeModel)

    logger.info("Processing %s", args.file)
    image = cv2.imread(args.file)
    (imageHeigth, imageWidth, colorBytes) = image.shape
    logger.info("Image: %d x %d", imageWidth, imageHeigth)
    blob = cv2.dnn.blobFromImage(
        image,
        scalefactor=1.0,
        size=(300, 300),
        mean=[104, 117, 123],
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
            d = detections[0, 0, i]
            xx1 = detections[0, 0, i, 3]
            yy1 = detections[0, 0, i, 4]
            xx2 = detections[0, 0, i, 5]
            yy2 = detections[0, 0, i, 6]
            x1 = int(xx1 * imageWidth)
            y1 = int(yy1 * imageHeigth)
            x2 = int(xx2 * imageWidth)
            y2 = int(yy2 * imageHeigth)
            logger.info("bbox: (%d,%d) - (%d,%d))", x1, y1, x2, y2)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv2.imwrite(args.file + ".p." + str(i) + ".jpg", image)
        cv2.imwrite(args.file + ".dnn.jpg", image)
