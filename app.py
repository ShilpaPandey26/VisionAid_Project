import cv2
import numpy as np
import pyttsx3
import threading
import time
from ultralytics import YOLO  # YOLOv8 for better detection

# Load YOLOv8 model
model = YOLO("yolov8s.pt")  # Using YOLOv8 small model for better accuracy and speed

# Initialize Text-to-Speech
engine = pyttsx3.init()

last_speech_time = 0  # Variable to track last announcement time

def provide_audio_feedback(message):
    """Function to provide voice alerts with a cooldown"""
    global last_speech_time
    if time.time() - last_speech_time > 2:  # 2-second cooldown
        print("🔊", message)
        engine.say(message)
        engine.runAndWait()
        last_speech_time = time.time()

def estimate_distance(bbox, frame_height):
    """Estimate distance based on bounding box size"""
    obj_height = bbox[3] - bbox[1]  # Height of bounding box
    relative_size = obj_height / frame_height
    distance = round((1 - relative_size) * 8, 2)  # Approximation for distance calculation
    return max(distance, 0.5)  # Ensure minimum 0.5m distance

def detect_obstacles(frame):
    """Runs YOLO object detection and labels obstacles in frame"""
    h, w = frame.shape[:2]
    results = model(frame)  # Detect objects using YOLO
    detected_objects = []
    confidence_threshold = 0.5  # Set confidence threshold
    regions = {"Left": 0, "Center": 0, "Right": 0}
    person_detected = False

    for r in results:
        for i, box in enumerate(r.boxes.xyxy):
            conf = r.boxes.conf[i].item()
            if conf < confidence_threshold:
                continue  # Ignore low-confidence detections

            x1, y1, x2, y2 = map(int, box[:4])  # Bounding box
            obj_class = int(r.boxes.cls[i].item())  # Object class index
            label = model.names[obj_class]
            distance = estimate_distance([x1, y1, x2, y2], h)

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {distance}m", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if label.lower() == "person":
                person_detected = True
                detected_objects.append(("Person", distance))
            else:
                detected_objects.append(("Obstacle", distance))

            # Assign detected obstacles to regions
            center_x = (x1 + x2) // 2  # Middle of bounding box
            if center_x < w // 3:
                regions["Left"] += 1
            elif center_x > 2 * w // 3:
                regions["Right"] += 1
            else:
                regions["Center"] += 1

    print("Obstacle Regions:", regions)  # Debugging log
    return frame, detected_objects, regions, person_detected

def announce_navigation(regions):
    """Provides navigation guidance based on detected obstacles"""
    if regions["Center"] > 0:
        if regions["Left"] == 0 and regions["Right"] > 0:
            provide_audio_feedback("Obstacle ahead! Turn left.")
        elif regions["Right"] == 0 and regions["Left"] > 0:
            provide_audio_feedback("Obstacle ahead! Turn right.")
        elif regions["Left"] == 0 and regions["Right"] == 0:
            provide_audio_feedback("Obstacle ahead! Move cautiously.")
        else:
            provide_audio_feedback("Stop! No safe path detected.")
    elif regions["Left"] > 0 and regions["Right"] > 0:
        provide_audio_feedback("Caution! Objects detected on both sides.")
    else:
        provide_audio_feedback("Path is clear. Proceed.")

def announce_detections(detected_objects, person_detected):
    """Announces detected objects with their estimated distance"""
    if person_detected:
        for label, distance in detected_objects:
            if label == "Person":
                provide_audio_feedback(f"Person detected at {distance} meters.")
    elif detected_objects:
        provide_audio_feedback("Obstacle detected. Navigate carefully.")
    else:
        provide_audio_feedback("No obstacles detected. Proceed.")

# Start webcam with multi-threading to reduce lag
class VideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Reduce resolution to 640x480
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.stream.set(cv2.CAP_PROP_FPS, 30)  # Limit FPS to 30 for performance
        self.ret, self.frame = self.stream.read()
        self.stopped = False
        self.thread = threading.Thread(target=self.update, args=())

    def start(self):
        self.thread.start()
        return self

    def update(self):
        while not self.stopped:
            self.ret, self.frame = self.stream.read()

    def read(self):
        return self.frame if self.ret else None

    def stop(self):
        self.stopped = True
        self.thread.join()
        self.stream.release()

# Use an IP Camera or USB Camera
video_source = "http://192.168.251.109:8080/video"  # Replace with your camera URL or use 0 for USB webcam
cap = VideoStream(video_source).start()

while True:
    frame = cap.read()
    if frame is None:
        continue  # Skip iteration if frame is not available

    frame, detected_objects, obstacle_regions, person_detected = detect_obstacles(frame)

    # Run announcements in a separate thread to prevent lag
    threading.Thread(target=announce_detections, args=(detected_objects, person_detected)).start()
    threading.Thread(target=announce_navigation, args=(obstacle_regions,)).start()

    # Display output
    cv2.imshow("Obstacle Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.stop()
cv2.destroyAllWindows()
