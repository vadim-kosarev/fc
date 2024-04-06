import argparse
import io
import logging.config
import random
import socket

import cv2 as cv2
# from minio import Minio

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


def s3Escape(str):
    str = str.replace(":", "_#_")
    return str


def getS3FilePath(msgHeaders):
    s = "{}/{}/{}_{}.jpg".format(
        s3Escape(msgHeaders['hostname']),
        s3Escape(msgHeaders['source']),
        s3Escape(msgHeaders['timestamp']),
        s3Escape(msgHeaders['localId']))
    return s


publisher = RabbitMQClient()
cameraIndex = args.cam
capture = cv2.VideoCapture(cameraIndex, cv2.CAP_ANY)

if not capture.isOpened():
    logger.error("Cannot open camera %s...", cameraIndex)
    exit(444)

logger.info("runnin %s", capture.getBackendName())

# minioClient = Minio("localhost:9000",
#                     secure=False,
#                     access_key="FbpmajwQ1g3JZAsPPuKG",
#                     secret_key="GqB2x8nsEa8Kbc78tidjVW7x8WsFtalWBwqbVUIJ",
#                     )

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
    msgHeaders = {
        "source": "Camera:{}".format(cameraIndex),
        "hostname": socket.gethostname(),
        "frameNo": str(frameNo),
        "localId": str(random.randint(1000000, 9999999))
    }

    publisher.publishFrame(frameJpeg, headers=msgHeaders)

    s3Path = getS3FilePath(msgHeaders)
    if (frameNo == 0):
        logger.info("Putting to S3: %s", s3Path)

    # jpgBytes = frameJpeg.tobytes()
    # minioClient.put_object(bucket_name="jpgdata",
    #                        object_name=s3Path,
    #                        data=io.BytesIO(jpgBytes),
    #                        length=len(jpgBytes))

    if (cv2.waitKey(1) == ord('q')):
        break

capture.release()
cv2.destroyAllWindows()
