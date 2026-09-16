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
pTime = 0 

def fingersUp(lmList):
    fingers = []

    # Thumb
    if lmList[4][1] < lmList[3][1]:
        fingers.append(1)
    else:
        fingers.append(0)
    # Fingers
    tips = [8, 12, 16, 20]
    joints = [6, 10, 14, 18]

    for tip, joint in zip(tips, joints):
        if lmList[tip][2] < lmList[joint][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

def leftClick():
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0) # Left button down
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0) # Left button up    


while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = detector.process(rgb)
       
    # 1 - Find hand landmarks
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mphands.HAND_CONNECTIONS
            )
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

    # 3 - Check which fingers are up
        fingers = fingersUp(lmList)
        #print(fingers)
        cv2.rectangle(frame, (frameR, frameR), (w-frameR, h-frameR), (255, 0, 255), 2) # Draw a rectangle for the active area

    # 4 - Only Index Finger: Moving Mode
        if fingers[1] ==1 and fingers[2] == 0:
            #print("Moving Mode")
    # 5 - Convert Coordinates
            x3 = np.interp(x1, (frameR, w-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, h-frameR), (0, hScr))
    # 6 - Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

    # 7 - Move Mouse
            ctypes.windll.user32.SetCursorPos(int(clocX), int(clocY))
            cv2.circle(frame, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
            
    # 8 - Both Index and Middle Fingers: Clicking Mode
        if fingers[1] ==1 and fingers[2] == 1:
            #print("Clicking Mode")
            x3 = np.interp(x1, (frameR, w-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, h-frameR), (0, hScr))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            ctypes.windll.user32.SetCursorPos(int(clocX), int(clocY))
            cv2.circle(frame, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
            
    # 9 - Find distance between fingers
        if fingers[1] ==1 and fingers[2] == 1 and x2-x1 < 20:
            print("Click")

    # 10 - Click mouse if distance short    
            leftClick()
            cv2.circle(frame, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
    # 11 - Frame Rate
    cTime = time.time()
    fps = 1/(cTime - pTime) 
    pTime = cTime
    cv2.putText(frame,str(int(fps)),(20,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    # 12 - Display
    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break   

cap.release()
cv2.destroyAllWindows()
