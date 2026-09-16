import cv2
import mediapipe as mp
import numpy as np
import time
import ctypes 

# Step 1: Create virtual environment, paste into terminal: python -m venv mouseenv
# Step 2: Install dependencies, paste into terminal: pip install -r mouse_requirements.txt

# To run environment, paste into terminal: mouseenv\Scripts\activate
# To run code, paste into terminal: python hand_tracking.py

wScr = ctypes.windll.user32.GetSystemMetrics(0)
hScr = ctypes.windll.user32.GetSystemMetrics(1)
frameR = 100 # Frame Reduction
smoothening = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0


cap = cv2.VideoCapture(0)



mphands = mp.solutions.hands
detector = mphands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = detector.process(rgb)
       
    # 1 - Find hand landmarks
    #if result.multi_hand_landmarks:
       # for hand_landmarks in result.multi_hand_landmarks:
            #mp_draw.draw_landmarks(
              ### mphands.HAND_CONNECTIONS
      #  )
    lmList = []

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]

        for id, lm in enumerate(hand_landmarks.landmark):   
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
    # 2 - Get the tip of index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:] # Index tip
        x2, y2 = lmList[12][1:] # Middle tip
        #print(x1, y1, x2, y2)

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break   

cap.release()
cv2.destroyAllWindows()
