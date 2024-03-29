import cv2 as cv2

from MessagePublisher import RabbitMQClient

publisher = RabbitMQClient()

capture = cv2.VideoCapture(0)
if not capture.isOpened():
    print("Cannot open camera...")
    exit(444)

cnt = 0

while True:
    ret, frame = capture.read()
    cnt += 1

    if (cnt % 25 == 0):
        print("Frame {}".format(cnt))

    if (not ret):
        print("Can't read frame")
        break

    cv2.imshow('frame', frame)
    retval, frameJpeg = cv2.imencode(".jpg", frame)
    publisher.publishFrame(frameJpeg)

    if (cv2.waitKey(1) == ord('q')):
        break

capture.release()
cv2.destroyAllWindows()
