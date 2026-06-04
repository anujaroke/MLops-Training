from flask import Flask, render_template, request
from ultralytics import YOLO
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

os.makedirs("static", exist_ok=True)

# Load trained model from the app directory to avoid CWD issues
model_path = os.path.join(app.root_path, "best.pt")
model = YOLO(model_path)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    file = request.files.get("image")
    if not file or not file.filename:
        return render_template("index.html", error="Please upload an image.")

    filename = secure_filename(file.filename)
    static_path = os.path.join(app.root_path, "static", filename)

    file.save(static_path)

    # Run YOLO prediction
    results = model.predict(static_path, verbose=False)

    emotion = "Unknown"
    confidence = 0

    best_conf = 0

    for r in results:
        for box in r.boxes:

            conf = float(box.conf[0])

            if conf > best_conf:

                best_conf = conf

                cls = int(box.cls[0])

                emotion = model.names[cls]

                confidence = conf

    return render_template(
        "index.html",
        emotion=emotion,
        confidence=round(confidence * 100, 2),
        image=file.filename
    )

if __name__ == "__main__":
    app.run(debug=True)