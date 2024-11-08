import cv2
import socket
import struct
from picamera2 import Picamera2

# Set up the Pi camera
pi_camera = Picamera2()
pi_camera.configure(pi_camera.create_video_configuration())
pi_camera.start()

# Set up UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)

# Define the address of the Windows PC (replace with the IP address of your PC)
windows_pc_ip = '192.168.10.135'  # Change this to your Windows PC's IP
port = 5005

# Define a maximum chunk size (e.g., 60,000 bytes)
CHUNK_SIZE = 60000

while True:
    # Capture frame
    frame = pi_camera.capture_array()
    # Resize the frame for smoother transmission
    frame = cv2.resize(frame, (640, 480))

    # Encode frame to JPEG
    _, buffer = cv2.imencode('.jpg', frame)
    buffer = buffer.tobytes()

    # Send frame in chunks
    for i in range(0, len(buffer), CHUNK_SIZE):
        chunk = buffer[i:i + CHUNK_SIZE]
        sock.sendto(struct.pack("L", len(chunk)) + chunk, (windows_pc_ip, port))
