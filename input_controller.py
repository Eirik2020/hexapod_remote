import socket
import keyboard  # Requires the keyboard library
import time

# Server IP and port
HOST = '192.168.10.117'  # Replace with the server's IP address
PORT = 12345

# Connect to the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to server. Press 'w', 'a', 's', 'd' to send commands, or 'q' to quit.")

    while True:
        # Check if any of the keys 'w', 'a', 's', 'd', or 'q' is pressed
        if keyboard.is_pressed('w'):
            s.sendall(b'w')
            print("Sent command: w")
            time.sleep(0.2)  # Add a short delay to prevent multiple sends
        elif keyboard.is_pressed('a'):
            s.sendall(b'a')
            print("Sent command: a")
            time.sleep(0.2)
        elif keyboard.is_pressed('s'):
            s.sendall(b's')
            print("Sent command: s")
            time.sleep(0.2)
        elif keyboard.is_pressed('d'):
            s.sendall(b'd')
            print("Sent command: d")
            time.sleep(0.2)
        elif keyboard.is_pressed('q'):
            print("Closing connection.")
            break  # Exit the loop to close the connection
