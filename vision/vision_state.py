import threading

class VisionState:
    def __init__(self):
        self.active = False
        self.frame = None
        self.objects = []
        self.lock = threading.Lock()

vision_state = VisionState()
