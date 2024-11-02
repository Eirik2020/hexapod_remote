from flask import Flask, Response
from picamera2 import Picamera2
import cv2

app = Flask(__name__)

# Initialize the camera
pi_camera = Picamera2()
pi_camera.configure(pi_camera.create_video_configuration())
pi_camera.start()

def generate_frames():
    while True:
        # Capture frame-by-frame
        frame = pi_camera.capture_array()
        # Resize or process the frame if needed
        frame = cv2.resize(frame, (640, 480))

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Concatenate frame bytes to create a streaming HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # Route to serve the video stream
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    # HTML page to display the video stream
    return '''
    <html>
    <head>
        <title>Raspberry Pi Camera Stream</title>
    </head>
    <body>
        <h1>Raspberry Pi Camera Stream</h1>
        <img src="/video_feed">
    </body>
    </html>
    '''

if __name__ == "__main__":
    # Start the Flask app
    app.run(host="0.0.0.0", port=5000)
