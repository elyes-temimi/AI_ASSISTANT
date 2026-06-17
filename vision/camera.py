import cv2

class Camera:
    def __init__(self):
        self.cap = None

    def open(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)

    def capture_frame(self):
        if self.cap is None:
            return None
        ret, frame = self.cap.read()
        return frame if ret else None

    def close(self):
        if self.cap:
            self.cap.release()
            self.cap = None
