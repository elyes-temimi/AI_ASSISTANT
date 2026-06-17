def is_open_camera_cmd(text):
    return any(p in text.lower() for p in [
        "open camera", "turn on camera", "activate camera"
    ])

def is_describe_cmd(text):
    return any(p in text.lower() for p in [
        "what do you see", "describe", "look here"
    ])

def is_close_camera_cmd(text):
    return any(p in text.lower() for p in [
        "close camera", "stop camera"
    ])
