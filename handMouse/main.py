# -*- coding: utf-8 -*-

from gestureController import gestureController

if __name__ == "__main__":
    controller = gestureController.GestureController()
    controller.main()
      
    try:
        while True:
            usr_input = input("")
            if usr_input == "quit":
                break
            else:
                pass
    except KeyboardInterrupt:
        print("Exiting software")
        
    controller.stop()
    controller.cleanup()