import argparse
import logging.config
import random
import socket

import cv2 as cv2

from MessagePublisher import RabbitMQClient

parser = argparse.ArgumentParser(
    description='Captures video stream and sends each frame '
                'to RabbitMQ')
parser.add_argument(
    "--cam",
    type=int,
    default=0,
    help="System camera Index: 0,1,2,...")
parser.add_argument("--pid", type=int, help="Process ID")
args = parser.parse_args()

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)
logger.info("Initialized")

publisher = RabbitMQClient()
cameraIndex = args.cam
capture = cv2.VideoCapture(
    cameraIndex,
    cv2.CAP_ANY,
    [
        # cv2.CAP_PROP_FRAME_WIDTH, 1280,
        # cv2.CAP_PROP_FRAME_HEIGHT, 720
    ]
)

if not capture.isOpened():
    logger.error("Cannot open camera %s...", cameraIndex)
    exit(444)

logger.info("runnin %s", capture.getBackendName())

cnt = 0
framesCnt = 10

while True:
    ret, frame = capture.read()
    cnt += 1
    frameNo = cnt % framesCnt
    if (frameNo == 0):
        logger.info("Frame {}".format(cnt))

    if (not ret):
        logger.error("Can't read frame")
        break

    cv2.imshow('CameraFrames', frame)
    retval, frameJpeg = cv2.imencode(".jpg", frame)
    publisher.publishFrame(frameJpeg, headers={
        "source": "Camera:{}".format(cameraIndex),
        "hostname": socket.gethostname(),
        "frameNo": str(frameNo),
        "localId": str(random.randint(1000000,9999999))
    })

    if (cv2.waitKey(1) == ord('q')):
        break

capture.release()
cv2.destroyAllWindows()
