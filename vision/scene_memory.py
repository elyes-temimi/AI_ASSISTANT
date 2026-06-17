import time

class SceneMemory:
    def __init__(self):
        self.objects = {}
        self.last_update = time.time()

    def update(self, detected_objects):
        now = time.time()
        for obj in detected_objects:
            if obj not in self.objects:
                self.objects[obj] = {
                    "count": 1,
                    "first_seen": now,
                    "last_seen": now
                }
            else:
                self.objects[obj]["count"] += 1
                self.objects[obj]["last_seen"] = now

        self.last_update = now

    def summary(self):
        if not self.objects:
            return "Nothing visible."

        lines = []
        for obj, data in self.objects.items():
            lines.append(
                f"- {obj} (seen {data['count']} times)"
            )

        return "\n".join(lines)

scene_memory = SceneMemory()
