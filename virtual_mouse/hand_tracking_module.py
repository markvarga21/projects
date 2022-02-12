import cv2
import mediapipe as mp
import time


class handDetector():
	def __init__(self, mode=False, maxHands=2, detectionConfidence=0.5, trackConfidence=0.5):
		self.mode = mode
		self.maxHands = maxHands
		self.detectionConfidence = detectionConfidence
		self.trackConfidence = trackConfidence

		self.mpHands = mp.solutions.hands
		self.hands = self.mpHands.Hands(self.mode, self.maxHands, 
										self.detectionConfidence, self.trackConfidence) # uses RGB images
		self.mpDraw = mp.solutions.drawing_utils

	def findHands(self, img, draw=True):
		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # converting to RGB
		self.results = self.hands.process(imgRGB)
		#print(results.multi_hand_landmarks)

		if self.results.multi_hand_landmarks: # ha lat tenyeret
			for handLms in self.results.multi_hand_landmarks: # tobb tenyer eseten, 21 van osszesen
				if draw:
					self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS) # drawing the points with lines between
		return img

	def findPosition(self, img, handNo=0, draw=True):

		lmList = []
		if self.results.multi_hand_landmarks:
			myHand = self.results.multi_hand_landmarks[handNo]

			for id, lm in enumerate(myHand.landmark):
					# print(id, lm)
					h, w, c = img.shape # height, width, channel
					cx, cy = int(lm.x * w), int(lm.y * h) # in order to use at pixels
					#print(id, cx, cy)
					lmList.append([id, cx, cy])
					if draw:
						cv2.circle(img, (cx, cy), 8, (255, 0, 0), cv2.FILLED)
		return lmList



def main():
	cap = cv2.VideoCapture(0)

	detector = handDetector()

	# FPS
	pTime = 0 # previsious time
	cTime = 0 # current time

	# running the webcam
	while True:
		success, img = cap.read()	
		img = detector.findHands(img)
		lmList = detector.findPosition(img)
		if len(lmList) != 0:
			print(lmList[4])


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

if __name__ == "__main__": # if we are running this script
	main()