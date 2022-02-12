import cv2
import cvzone

cap = cv2.VideoCapture(0)

while True:
	if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
		cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

	succes, img = cap.read()
	img = cv2.resize(img, (640, 360))
	cv2.imshow("Image", img)