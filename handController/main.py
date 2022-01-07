# -*- coding: utf-8 -*-

from gestureController import gestureController

if __name__ == "__main__":  
    controller = gestureController.GestureController()
    controller.main()
        
    controller.stop()
    controller.cleanup()