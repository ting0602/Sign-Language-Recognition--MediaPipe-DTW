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
# for i in range(2):
    conn, addr = server.accept()
    msg = conn.recv(15000)#.decode('utf-8')

    # print(msg)
    # if len(msg) < 20: print(msg)
    # else: print("##", len(msg))
    
    
    # Do initialize
    if msg == b"init": 
        SLR_init()
    # Request text result
    elif msg == b"result": 
        result = "detect_result()"
        conn.send(result)
    # Send frame
    else: 
        try:
            image_size = int(msg.decode('utf-8'))
        except:
            continue
        
        byte_image = b''
        while (len(byte_image) < image_size):
            byte_image += conn.recv(image_size)
        if (image_size != len(byte_image)): 
            print("error")
            continue
        # print("done")
        # Change data to cv2 format
        image = cv2.imdecode(np.frombuffer(byte_image, np.uint8), cv2.IMREAD_COLOR)

        rotate = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # cv2.imshow('img', rotate)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # exit()
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