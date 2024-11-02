from flask import Flask, Response
from picamera2 import Picamera2
import cv2

app = Flask(__name__)

# Initialize the camera
pi_camera = Picamera2()
# Configure camera with the desired resolution
pi_camera.configure(pi_camera.create_video_configuration({"size": (640, 480)}))
pi_camera.start()

def generate_frames():
    while True:
        # Capture frame-by-frame
        frame = pi_camera.capture_array()
        
        # Resize to reduce data per frame for faster streaming
        frame = cv2.resize(frame, (320, 240))

        # Encode frame to JPEG with lower quality for faster streaming
        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
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
    # HTML page to display the video stream at a larger size
    return '''
    <html>
    <head>
        <title>Raspberry Pi Camera Stream</title>
    </head>
    <body>
        <h1>Raspberry Pi Camera Stream</h1>
        <img src="/video_feed" width="640" height="480">
    </body>
    </html>
    '''

if __name__ == "__main__":
    # Start the Flask app in threaded mode
    app.run(host="0.0.0.0", port=5000, threaded=True)
