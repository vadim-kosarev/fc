import cv2
import numpy

face_detector = cv2.dnn.readNetFromCaffe(
    prototxt="github.com/gopinath-balu/computer_vision/CAFFE_DNN/deploy.prototxt.txt",
    caffeModel="github.com/gopinath-balu/computer_vision/CAFFE_DNN/res10_300x300_ssd_iter_140000.caffemodel"
)

# image = cv2.imread("../out/file_0_1.jpg")
image = cv2.imread("../out/f1.jpg")

(h,w, color) = image.shape
blob = cv2.dnn.blobFromImage(image)

face_detector.setInput(blob)
detections = face_detector.forward()

for i in range(0, detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    print("C: {} : {}".format(i, confidence))

    if confidence > 0.50:
        box = detections[0, 0, i, 3:7] * numpy.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

print("Show the final output")
cv2.imshow("Output", image)
cv2.waitKey(0)
print("Completed")
