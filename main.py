import cv2
import io
import numpy as np
import pyzbar.pyzbar as pyzbar
from flask import Flask, render_template, Response

app = Flask(__name__)

cap = cv2.VideoCapture(0)  # Kamera-Stream

def generate_frames():
    while True:
        success, frame = cap.read()  # Erfasse ein Frame von der Kamera
        if not success:
            break
        else:
            decoded_objects = pyzbar.decode(frame)  # QR-Codes im Frame erkennen
            for obj in decoded_objects:
                # Für jeden erkannten QR-Code den Inhalt ausgeben
                print("QR-Code erkannt:", obj.data.decode('utf-8'))

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
