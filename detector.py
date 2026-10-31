import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")


def detect_objects(frame):
    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        conf=0.5,
        verbose=False
    )

    annotated_frame = results[0].plot()
    object_count = len(results[0].boxes)

    class_counts = {}

    for box in results[0].boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        class_counts[class_name] = class_counts.get(class_name, 0) + 1

    return annotated_frame, object_count, class_counts
