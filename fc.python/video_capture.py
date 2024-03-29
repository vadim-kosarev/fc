import numpy
import cv2 as cv2

capture = cv2.VideoCapture(0)
if not capture.isOpened():
    print("Cannot open camera...")
    exit(444)

while True:
    ret, frame = capture.read()
