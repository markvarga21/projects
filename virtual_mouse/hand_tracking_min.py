import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0) # default webcam = 0

mpHands = mp.solutions.hands
hands = mpHands.Hands() # uses RGB images
mpDraw = mp.solutions.drawing_utils

# FPS
pTime = 0 # previsious time
cTime = 0 # current time

# running the webcam
while True:
	success, img = cap.read()

	imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # converting to RGB
	results = hands.process(imgRGB)
	#print(results.multi_hand_landmarks)

	if results.multi_hand_landmarks: # ha lat tenyeret
		for handLms in results.multi_hand_landmarks: # tobb tenyer eseten, 21 van osszesen
			for id, lm in enumerate(handLms.landmark):
				# print(id, lm)
				h, w, c = img.shape # height, width, channel
				cx, cy = int(lm.x * w), int(lm.y * h) # in order to use at pixels
				print(id, cx, cy)
				# if id == 0: # csuklo ID
					# cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

			mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) # drawing the points with lines between

	# calculating FPS
	cTime = time.time()
	fps = 1/(cTime-pTime)
	pTime = cTime
	# displaying FPS on the image
	text_scale = 3
	text_location = (10, 70)
	text_color = (0, 255, 255)
	text_thickness = 3
	cv2.putText(img, str(int(fps)), text_location, cv2.FONT_HERSHEY_PLAIN, text_scale, text_color, text_thickness)


	cv2.imshow("Image", img)
	cv2.waitKey(1)