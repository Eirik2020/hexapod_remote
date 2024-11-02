import cv2
import socket
import numpy as np
import struct

# Set up UDP socket for receiving
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 5005))  # Listening on all interfaces

while True:
    # Receive frame size
    payload_size = struct.calcsize("L")
    data, _ = sock.recvfrom(65536)
    frame_size = struct.unpack("L", data[:payload_size])[0]
    frame_data = data[payload_size:]

    # Reconstruct frame
    frame = np.frombuffer(frame_data, dtype=np.uint8)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    # Display the frame
    if frame is not None:
        cv2.imshow("Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

sock.close()
cv2.destroyAllWindows()
