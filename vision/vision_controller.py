from vision.vision_state import vision_state
from vision.realtime_camera import RealTimeCamera

class VisionController:
    def __init__(self):
        self.camera_thread = None

    def open_camera(self):
        if vision_state.active:
            return "Camera is already on."

        vision_state.active = True
        self.camera_thread = RealTimeCamera()
        self.camera_thread.start()
        return "Camera is on. I can see now."

    def describe(self):
        if not vision_state.active:
            return "Camera is not active."

        with vision_state.lock:
            objs = vision_state.objects.copy()

        if not objs:
            return "I don't see any recognizable objects."

        return "I see " + ", ".join(objs)

    def close_camera(self):
        if not vision_state.active:
            return "Camera is already off."

        vision_state.active = False
        return "Camera closed."
