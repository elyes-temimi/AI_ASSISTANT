from vision.vision_state import vision_state
from vision.scene_memory import scene_memory

def build_vision_context():
    if not vision_state.active:
        return ""

    summary = scene_memory.summary()

    return f"""
[Vision Context]
The assistant currently sees the following objects:
{summary}

Use this information to reason accurately.
"""