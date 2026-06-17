from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # fast & good enough

def detect_objects(frame):
    results = model(frame, verbose=False)
    names = results[0].names

    detected = []
    for r in results[0].boxes:
        cls = int(r.cls[0])
        detected.append(names[cls])

    return list(set(detected))
