# -*- coding: utf-8 -*-

import cv2
import os
import queue
import numpy as np
import imutils

from queue import Queue
from threading import Thread

class VideoStreamer:
    def __init__(self, width=640, height=480, queueSize=128):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        self.stopped = False
                
        self.frame = None
        
        # initialize the queue used to store frames read from
        # the video file
        self.Q = Queue(maxsize=queueSize)
        
        # Start the thread to read frames from the video stream
        self.start()
        
    def get_frame(self):
        return self.frame
    
    def start(self):
        # start a thread to read frames from the file video stream
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True
        self.t.start()
        
        self.stream_t = Thread(target=self.start_stream, args=())
        self.stream_t.daemon = True
        self.stream_t.start()
    
    def read(self):
        # return next frame in the queue
        return self.Q.get()
    
    def more(self):
        # return True if there are still frames in the queue
        return self.Q.qsize() > 0
    
    def update(self):
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self.stopped:
                return

            ret, frame = self.capture.read()
            if not ret:
                break
            
            # otherwise, ensure the queue has room in it
            if not self.Q.empty():
                try:
                    self.Q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
          
            self.Q.put(frame)
                
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        self.t.join()
        self.stream_t.join()
        
        print("Ending video streamer...")
        self.capture.release()

    def start_stream(self):
        while True:
            if self.stopped:
                return
            self.frame = self.read()
            
            # disp_frame = self.frame.copy()
            # disp_frame = imutils.resize(disp_frame, width=450)
            # disp_frame = cv2.cvtColor(disp_frame, cv2.COLOR_BGR2GRAY)
            # disp_frame = np.dstack([disp_frame, disp_frame, disp_frame])
            # # display the size of the queue on the frame
            # cv2.putText(disp_frame, "Queue Size: {}".format(self.Q.qsize()),
            #     (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)    
            # # show the frame and update the FPS counter
            # cv2.imshow("Frame", disp_frame)
            # key = cv2.waitKey(1) & 0xFF
            # if key == ord('q'):
            #     break

if __name__ == "__main__":
    videoStreamer = VideoStreamer()
    
    try:
        while True:
            usr_input = input("")
            if usr_input == "quit":
                break
            else:
                pass
    except KeyboardInterrupt:
        print("Exiting software")
        
    videoStreamer.stop()
    cv2.destroyAllWindows()