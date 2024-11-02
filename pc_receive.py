import cv2
import socket
import numpy as np
import struct

# Set up UDP socket for receiving
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 5005))  # Listening on all interfaces

buffer = b''

while True:
    # Receive chunk
    data, _ = sock.recvfrom(65536)
    chunk_size = struct.unpack("L", data[:struct.calcsize("L")])[0]
    chunk = data[struct.calcsize("L"):]

    # Append the chunk to the buffer
    buffer += chunk

    # If the buffer reaches the expected size of the frame, display it
    if len(buffer) >= chunk_size:
        frame = np.frombuffer(buffer, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        buffer = b''  # Reset the buffer after displaying the frame

        # Display the frame
        if frame is not None:
            cv2.imshow("Stream", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

sock.close()
cv2.destroyAllWindows()
