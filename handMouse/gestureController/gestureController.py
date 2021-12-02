import cv2
import numpy as np
import time
import autopy
import pyautogui

from aiComputerGestureControl.utils import get_config_param
from aiComputerGestureControl.gestureController import handTrackingModule as htm

class GestureController():
    def __init__(self):
        # Load config params
        self.frameR = int(get_config_param("GestureController", "frameReduction"))
        self.smoothening = int(get_config_param("GestureController", "pointerSmootheningFactor"))
        self.scroll_scale_factor = int(get_config_param("GestureController", "scrollScaleDownFactor"))
        self.wCam = int(get_config_param("GestureController", "captureWindowWidth"))
        self.hCam = int(get_config_param("GestureController", "captureWindowHeight"))
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.wCam)
        self.cap.set(4, self.hCam)
        self.detector = htm.handDetector(maxHands=1)
        self.wScr, self.hScr = autopy.screen.size()
    
        self.stopped = False
        
    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def main(self):
        pTime = 0
        plocX, plocY = 0, 0
        clocX, clocY = 0, 0

        while not self.stopped:
            # 1. Find hand Landmarks
            success, img = self.cap.read()
            img = self.detector.findHands(img)
            lmList, bbox = self.detector.findPosition(img)
            
            # 2. Get the tip of the index and middle fingers
            if len(lmList) != 0:
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]
                # print(x1, y1, x2, y2)
            
            # 3. Check which fingers are up
            fingers = self.detector.fingersUp()
            # print(fingers)
            cv2.rectangle(img, (self.frameR, self.frameR), (self.wCam - self.frameR, self.hCam - self.frameR),
            (255, 0, 255), 2)
            
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
                    length, img, lineInfo = self.detector.findDistance(8, 12, img)
                    # 5b. Click mouse if distance short
                    if length < 40:
                        cv2.circle(img, (lineInfo[4], lineInfo[5]),
                        15, (0, 255, 0), cv2.FILLED)
                        autopy.mouse.click()
                 
                # 6. All fingers : scroll mode
                elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:
                    pass
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
      
    try:
        while True:
            usr_input = input("")
            if usr_input == "quit":
                break
            else:
                pass
    except KeyboardInterrupt:
        print("Exiting software")
        
    gestureController.stop()
    gestureController.cleanup()
    