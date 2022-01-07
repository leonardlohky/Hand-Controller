# -*- coding: utf-8 -*-

import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import cvzone
from pynput.keyboard import Key, Controller

keyboard_layout1 = [[((25,100),(45,45)), ((85,100),(45,45)), ((145,100),(45,45)), ((205,100),(45,45)), ((265,100),(45,45)), ((325,100),(45,45)), ((385,100),(45,45)), ((445,100),(45,45)), ((505,100),(45,45)), ((565,100),(45,45))],
                    [((25,160),(45,45)), ((85,160),(45,45)), ((145,160),(45,45)), ((205,160),(45,45)), ((265,160),(45,45)), ((325,160),(45,45)), ((385,160),(45,45)), ((445,160),(45,45)), ((505,160),(45,45)), ((565,160),(45,45))],
                    [((25,220),(65,45)), ((105,220),(45,45)), ((165,220),(45,45)), ((225,220),(45,45)), ((285,220),(45,45)), ((345,220),(45,45)), ((405,220),(45,45)), ((465,220),(45,45)), ((525,220),(105,45))],
                    [((25,280),(45,45)), ((85,280),(70,45)), ((170,280),(305,45)), ((490,280),(45,45)), ((545,280),(60,45))]
                   ]

keyboard_layout2 = [[((25,100),(45,45)), ((85,100),(45,45)), ((145,100),(45,45)), ((205,100),(45,45)), ((265,100),(45,45)), ((325,100),(45,45)), ((385,100),(45,45)), ((445,100),(45,45)), ((505,100),(45,45)), ((565,100),(45,45))],
                    [((25,160),(45,45)), ((85,160),(45,45)), ((145,160),(45,45)), ((205,160),(45,45)), ((265,160),(45,45)), ((325,160),(45,45)), ((385,160),(45,45)), ((445,160),(45,45)), ((505,160),(45,45)), ((565,160),(45,45))],
                    [((25,220),(65,45)), ((135,220),(55,45)), ((210,220),(55,45)), ((285,220),(55,45)), ((360,220),(55,45)), ((435,220),(55,45)), ((525,220),(105,45))],
                    [((25,280),(45,45)), ((85,280),(70,45)), ((170,280),(305,45)), ((490,280),(45,45)), ((545,280),(60,45))]
                   ]

keys_abc = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
        ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"],
        ["shift", "z", "x", "c", "v", "b", "n", "m", "backspace"],
        ["123", "mouse", "space", ".", "go"]]

keys_ABC = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
              ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":"],
              ["shift", "Z", "X", "C", "V", "B", "N", "M", "backspace"],
              ["123", "mouse", "space", ".", "go"]]

keys_123 = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            ["-", "/", ":", ";", "(", ")", "$", "&", "@", "\""],
            ["#+=", ".", ",", "?", "!", "'", "backspace"],
            ["ABC", "mouse", "space", ".", "go"]]

keys_symbols = [["[", "]", "{", "}", "#", "%", "^", "*", "+", "="],
                ["_", "\\", "|", "~", "<", ">", "$", "&", "@", "."],
                ["123", ".", ",", "?", "!", "'", "backspace"],
                ["ABC", "mouse", "space", ".", "go"]]
 
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 10, y + 28),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
    return img
 
class Button():
    def __init__(self, pos, text, size=[45, 45]):
        self.pos = pos
        self.size = size
        self.text = text
 
class GestureKeyboard():
    def __init__(self):
        self.mode = "abc"
        self.stopped = False
        
        self.detector = HandDetector(detectionCon=0.8)
        self.keyboard = Controller()
        self.buttonList_abc = []
        self.buttonList_ABC = []
        self.buttonList_123 = []
        self.buttonList_sym = []
        
        self.init_button_list()
    
    def init_button_list(self):
        for i in range(len(keys_abc)):
            for j, key in enumerate(keys_abc[i]):
                button_pos = list(keyboard_layout1[i][j][0])
                button_size = list(keyboard_layout1[i][j][1])
                self.buttonList_abc.append(Button(button_pos, key, button_size))
                
        for i in range(len(keys_ABC)):
            for j, key in enumerate(keys_ABC[i]):
                button_pos = keyboard_layout1[i][j][0]
                button_size = keyboard_layout1[i][j][1]
                self.buttonList_ABC.append(Button(button_pos, key, button_size))
      
        for i in range(len(keys_123)):
            for j, key in enumerate(keys_123[i]):
                button_pos = keyboard_layout2[i][j][0]
                button_size = keyboard_layout2[i][j][1]
                self.buttonList_123.append(Button(button_pos, key, button_size))
    
        for i in range(len(keys_symbols)):
            for j, key in enumerate(keys_symbols[i]):
                button_pos = keyboard_layout2[i][j][0]
                button_size = keyboard_layout2[i][j][1]
                self.buttonList_sym.append(Button(button_pos, key, button_size))
        
        self.currentButtonList = self.buttonList_abc
                
    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
    
    def start(self, vid_src):
        self.cap = vid_src

        self.stopped = False
        self.main()
        
    def stop(self):
        self.stopped = True
        
    def main(self):
        while not self.stopped:
            success, img = self.cap.read()
            hands, img = self.detector.findHands(img)
            img = drawAll(img, self.currentButtonList)
         
            if hands:
                # Hand 1
                hand1 = hands[0]
                lmList = hand1["lmList"]  # List of 21 Landmark points
                
                for button in self.currentButtonList:
                    x, y = button.pos
                    w, h = button.size
         
                    if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                        cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 10, y + 30),
                                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
                        
                        l, _, _ = self.detector.findDistance(lmList[8], lmList[12], img)
         
                        ## when clicked
                        if l < 30:
                            cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, button.text, (x + 10, y + 30),
                                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
                            
                            if button.text == "backspace":
                                self.keyboard.press(Key.backspace)
                                self.keyboard.release(Key.backspace)
                                
                            elif button.text == "space":
                                self.keyboard.press(Key.space)
                                self.keyboard.release(Key.space)
                                
                            elif button.text == "go":
                                self.keyboard.press(Key.enter)
                                self.keyboard.release(Key.enter)
                                
                            elif button.text == "mouse":
                                self.stop()
                                
                            elif button.text == "shift":
                                if self.mode != "ABC":
                                    self.mode = "ABC"
                                    self.currentButtonList = self.buttonList_ABC
                                else:
                                    self.mode = "abc"
                                    self.currentButtonList = self.buttonList_abc
                              
                            elif button.text == "ABC":
                                self.mode = "ABC"
                                self.currentButtonList = self.buttonList_ABC 
                                
                            elif button.text == "123":
                                self.mode = "123"
                                self.currentButtonList = self.buttonList_123  
                                
                            elif button.text == "#+=":
                                self.mode = "#+="
                                self.currentButtonList = self.buttonList_sym 
                                
                            else:
                                self.keyboard.press(button.text)
    
                            sleep(0.15)
         
            cv2.imshow("Image", img)
            if cv2.waitKey(1) == ord('q'):
                break
        
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
        
    gestureKeyboard = GestureKeyboard()
    gestureKeyboard.start(cap)
    
    gestureKeyboard.stop()
    gestureKeyboard.cleanup()