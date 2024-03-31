import argparse
import logging.config
import time

import cv2
import numpy

parser = argparse.ArgumentParser(
    description='processes faces image')
parser.add_argument("--file", type=str, default="out/input.jpg", help="source file")
args = parser.parse_args()

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)


class FacesImageProcessor:

    def __init__(self, **kwargs):
        self.jpgBuf = None


if (__name__ == "__main__"):
    logger.info("Started")
    obj = FacesImageProcessor()

    f = open(args.file, "rb")
    jpgBinData = f.read()
    f.close()

    narr = numpy.frombuffer(jpgBinData, numpy.int8)
    decodedImage = cv2.imdecode(narr, flags=cv2.IMREAD_UNCHANGED)

    cv2.imshow('CameraFrames', decodedImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
