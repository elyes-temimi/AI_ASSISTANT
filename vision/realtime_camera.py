import cv2
import threading
import time
from vision.vision_state import vision_state
from vision.object_detector import detect_objects
from vision.scene_memory import scene_memory




class RealTimeCamera(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.cap = None

    def run(self):
        self.cap = cv2.VideoCapture(0)

        while vision_state.active:
            ret, frame = self.cap.read()
            if not ret:
                continue

            objects = detect_objects(frame)
            scene_memory.update(objects)

            with vision_state.lock:
                vision_state.frame = frame
                vision_state.objects = objects

            # Draw objects on screen
            display = frame.copy()
            for obj in objects:
                cv2.putText(
                    display, obj, (20, 40 + 25 * objects.index(obj)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
                )

            cv2.imshow("Nova Vision", display)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC
                vision_state.active = False
                break

            time.sleep(0.03)  # ~30 FPS

        self.cap.release()
        cv2.destroyAllWindows()
