import math
import copy    
import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# pTime = 0
# cTime = 0
previousLMs = []

def checkDeltaLM(previousLMs, LM, id, delta=40):
    prevCX, prevCY = previousLMs[id]
    cx, cy = LM
    deltaX = prevCX - cx
    deltaY = prevCY- cy
    if deltaX > delta:
        print("DASH RIGHT")
        return 1
    if deltaY > delta:
        print("JUMP")
        return 2
    if deltaY < -1 * delta:
        print("STOMP")
        return 3
    return 0

start = 0
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            newPreviousLM = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                if time.time() - start >= 1:
                    if len(previousLMs) == len(handLms.landmark):
                        dash = checkDeltaLM(previousLMs, (cx, cy), id)
                        if dash != 0:
                            start = time.time()
                            break
                    newPreviousLM.append((cx, cy))
                previousLMs = copy.deepcopy(newPreviousLM)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
