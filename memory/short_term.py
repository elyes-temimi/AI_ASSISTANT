class ShortTermMemory:
    def __init__(self, limit=10):
        self.limit = limit
        self.memory = []

    def add(self, user, assistant):
        self.memory.append({"user": user, "assistant": assistant})
        if len(self.memory) > self.limit:
            self.memory.pop(0)

    def get(self):
        return self.memory
