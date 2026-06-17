import threading

class VoiceState:
    def __init__(self):
        self.lock = threading.Lock()
        self.vc_active = False

    def enter_vc(self):
        with self.lock:
            if self.vc_active:
                return False
            self.vc_active = True
            return True

    def exit_vc(self):
        with self.lock:
            self.vc_active = False

    def is_vc_active(self):
        with self.lock:
            return self.vc_active


voice_state = VoiceState()
