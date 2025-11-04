from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
from datetime import datetime
import os

app = Flask(__name__)
model = YOLO("yolov8n.pt")  # small + fast
LOG_FILE = "detected_objects.txt"

# clear log on start
open(LOG_FILE, "w").close()

def log_detection(label):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {label}\n")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/detect", methods=["POST"])
def detect():
    if "frame" not in request.files:
        return jsonify({"error": "no frame"}), 400

    file = request.files["frame"].read()
    npimg = np.frombuffer(file, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    results = model(frame)
    names = model.names
    detected_labels = []

    annotated = results[0].plot()  # draw boxes
    for box in results[0].boxes:
        cls = int(box.cls[0])
        label = names[cls]
        detected_labels.append(label)
        log_detection(label)

    # encode image back to jpg
    _, buffer = cv2.imencode(".jpg", annotated)
    annotated_bytes = buffer.tobytes()

    return annotated_bytes, 200, {"Content-Type": "image/jpeg"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
