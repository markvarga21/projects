import cv2
import mediapipe as mp
import time
import hand_tracking_module as htm
import math
import mouse

cap = cv2.VideoCapture(0)

detector = htm.handDetector()


def dist(p1, p2):
	id1, a1, a2 = p1
	id2, b1, b2 = p2
	d = math.sqrt( math.pow(b1-a1, 2) + math.pow(b2-a2, 2) )
	return int(d)


# FPS
pTime = 0 # previsious time
cTime = 0 # current time

	# running the webcam
while True:
	success, img = cap.read()	
	img = detector.findHands(img)
	lmList = detector.findPosition(img)
	if len(lmList) != 0:
		#print(lmList[4])
		point1, point2 = lmList[12], lmList[8]
		mutatoujj = lmList[12]
		idd, mutX, mutY = mutatoujj

		distance = dist(point1, point2)

		mouse_pos = mouse.get_position()
		mx, my = mouse_pos[0], mouse_pos[1]


		if distance <= 40:
			#print(f"{mx}, {my}")
			#mouse.click('left')
			mouse.move(-mutX, mutY)
			


	# calculating FP
	cTime = time.time()
	fps = 1/(cTime-pTime)
	pTime = cTime
	# displaying FPS on the image
	text_scale = 3
	text_location = (10, 70)
	text_color = (0, 255, 255) # BGR format
	text_thickness = 3
	cv2.putText(img, str(int(fps)), text_location, cv2.FONT_HERSHEY_PLAIN, text_scale, text_color, text_thickness)

	cv2.imshow("Image", img)
	cv2.waitKey(1)