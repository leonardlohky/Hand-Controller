# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time
import autopy
import pyautogui

from utils import get_config_param
from handController.gestureKeyboard import gestureKeyboard
from handController.handTrackingModule.HandTrackingModule import HandDetector
        
class GestureController():
    def __init__(self):
        # Load config params
        self.frameR = int(get_config_param("GestureController", "frameReduction"))
        self.smoothening = int(get_config_param("GestureController", "pointerSmootheningFactor"))
        self.scroll_scale_factor = int(get_config_param("GestureController", "scrollScaleDownFactor"))
        
        self.cap = cv2.VideoCapture(0)
        self.wCam = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.hCam = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.detector = HandDetector(maxHands=1)
        self.wScr, self.hScr = autopy.screen.size()
    
        self.stopped = False
        self.gestureKeyboard = gestureKeyboard.GestureKeyboard()
        
    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def bringup_keyboard(self, vid_src):
        self.gestureKeyboard.start(vid_src)
        
    def main(self):
        pTime = 0
        plocX, plocY = 0, 0
        clocX, clocY = 0, 0

        while not self.stopped:
            # 1. Find hand Landmarks
            success, img = self.cap.read()
            hands, img = self.detector.findHands(img)
            
            cv2.rectangle(img, (self.frameR, self.frameR), (self.wCam - self.frameR, self.hCam - self.frameR),
                (255, 0, 255), 2)
            
            # 2. Get the tip of the index and middle fingers
            if hands:
                # Hand 1
                hand1 = hands[0]
                lmList = hand1["lmList"]  # List of 21 Landmark points
                
                if len(lmList) != 0:
                    x1, y1 = lmList[8]
                    x2, y2 = lmList[12]
                    # print(x1, y1, x2, y2)
                
                # 3. Check which fingers are up
                fingers = self.detector.fingersUp_exp(hand1)
                print(fingers)
                
                # 4. Only Index Finger : Moving Mode
                if (len(fingers) > 0):
                    if fingers[1] == 1 and fingers[2] == 0:
                        # 4a. Convert Coordinates
                        x3 = np.interp(x1, (self.frameR, self.wCam - self.frameR), (0, self.wScr))
                        y3 = np.interp(y1, (self.frameR, self.hCam - self.frameR), (0, self.hScr))
                        
                        # 4b. Smoothen Values
                        clocX = plocX + (x3 - plocX) / self.smoothening
                        clocY = plocY + (y3 - plocY) / self.smoothening
                    
                        # 4c. Move Mouse
                        try:
                            autopy.mouse.move(self.wScr - clocX, clocY)
                            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                            plocX, plocY = clocX, clocY
                        except ValueError:
                            pass
                        
                    # 5. Both Index and middle fingers are up : Clicking Mode
                    elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
                        # 5a. Find distance between fingers
                        length, lineInfo, img = self.detector.findDistance(lmList[8], lmList[12], img)
                        # 5b. Click mouse if distance short
                        if length < 30:
                            cv2.circle(img, (lineInfo[4], lineInfo[5]),
                            15, (0, 255, 0), cv2.FILLED)
                            autopy.mouse.click()
                            time.sleep(0.15)
                    
                    # 6. Index, middle and ring fingers are up : scroll mode
                    elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                        # 6a. Convert Coordinates
                        x3 = np.interp(x1, (self.frameR, self.wCam - self.frameR), (0, self.wScr))
                        y3 = np.interp(y1, (self.frameR, self.hCam - self.frameR), (0, self.hScr))
                        # 6b. Smoothen Values
                        clocX = plocX + (x3 - plocX) / self.smoothening
                        clocY = plocY + (y3 - plocY) / self.smoothening
    
                        scroll_amt = int((clocY - (self.hScr / 2)) / self.scroll_scale_factor)
                        pyautogui.scroll(scroll_amt)
                        
                        cv2.circle(img, (x1, y1), 15, (255, 86, 255), cv2.FILLED)
                        plocX, plocY = clocX, clocY
                        
                    # 7. Index, middle, ring and pinky fingers are up : keyboard
                    elif fingers[1] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                        self.bringup_keyboard(self.cap)
                
                # 7. Frame Rate
                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
                
            # 8. Display
            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    def stop(self):
        self.stopped = True
    
if __name__ == "__main__":
    gestureController = GestureController()
    gestureController.main()
        
    gestureController.stop()
    gestureController.cleanup()