import threading
import cv2
import logging
from config import context

class UnderwaterCameraThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.cap = None
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        try:
            logging.info("+++++++++ SETTING UP UNDERWATER CAMERA ++++++++")
            while not self.stop_event.is_set():
                if context.VALUES['underwater_camera_connect']:
                    if self.cap is None:
                        try:
                            self.cap = cv2.VideoCapture(0)
                            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
                        except Exception as e:
                            logging.error(e)
                    ret, frame = self.cap.read()
                    if ret:
                        context.VALUES['underwater_camera_frame'] = frame
                    else:
                        cnt += 1
                        if cnt < 4:
                            logging.error("Could not read camera")
                else:
                    if self.cap is not None:
                        self.cap.release()
                        self.cap = None

        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received. Stopping thread.")
            if self.cap is not None:
                self.cap.release()
                self.cap = None
            self.stop()
        finally:
            if self.cap is not None:
                self.cap.release()
                self.cap = None
        logging.info("RELEASING UNDERWATER CAMERA *******************")