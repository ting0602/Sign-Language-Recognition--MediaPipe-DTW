import socket
import cv2
import numpy as np
from main import SLR_init, frame_input, detect_result

FRAME_REQUIRED = 20

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("140.113.141.90", 12345))
server.listen(10)

frames = []
frame_count = 0


# Server loop
while True:
    conn, addr = server.accept()
    msg = conn.recv(1024).decode('utf-8')

    # Do initialize
    if msg == "init": 
        SLR_init()
    # Request text result
    elif msg == "result": 
        result = detect_result()
        conn.send(result)
    # Send frame
    else: 
        # Change data to cv2 format
        image = cv2.imdecode(np.asarray(msg), cv2.IMREAD_COLOR)
        rotate = cv2.rotate(image, cv2.ROTATE_180)
        frames.append(image.tolist())

        # jia ie ge frame
        frame_count += 1
        
        # Send if 20 frames are collected
        if frame_count == FRAME_REQUIRED: 
            frame_input(msg)
            # result = frame_input(msg)

            # Clear buffer
            frames.clear()
            frame_count = 0