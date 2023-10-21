import socket
import cv2
import numpy as np
from main import SLR_init, frame_input, detect_result

FRAME_REQUIRED = 20

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("140.113.141.90", 12345))
# server.bind(("140.113.141.90", 23456))
server.listen(10)

frames = []
frame_count = 0
image_size = 0

# Server loop
while True:
# for i in range(2):
    conn, addr = server.accept()
    msg = conn.recv(30000)#.decode('utf-8')

    if len(msg) == 0: 
        conn.close()
        continue

    # print("msg:", msg)
    # if len(msg) < 20: print(msg)
    # else: print("##", len(msg))
    
    flg=0
    
    # Do initialize
    if msg == b"init": 
        SLR_init()
    # Request text result
    elif msg == b"request": 
        result = detect_result()
        # print(result)
        conn.send(result.encode('utf-8'))
    elif msg == b"request_sign_mode":
        # result = ?
        conn.send(result.encode('utf-8'))
    # Send frame
    else: 
        try:
            image_size = int(msg[0:5].decode('utf-8'))
            flg=1
        except:
            image_size = int(msg[0:4].decode('utf-8'))
            flg=0
        # print("length:", image_size)

        byte_image = b''
        byte_len = 0
        fail = False
        if len(msg) > (4+flg): byte_image = msg[4+flg:]
        while (byte_len+2 < image_size):
            tmp = conn.recv(image_size)
            tmp_len = len(tmp)
            if tmp_len == 0: 
                fail = True
                break
            byte_image += tmp
            byte_len += tmp_len
            # print(image_size, "now_get", len(byte_image))
        # conn.send("ok".encode('utf-8'))

        if fail: 
            conn.close()
            continue
        if ((image_size < byte_len) or (image_size > byte_len+2)): 
            print("error")
            conn.close()
            exit(0)
        
        # print("done")
        # Change data to cv2 format
        image = cv2.imdecode(np.frombuffer(byte_image, np.uint8), cv2.IMREAD_COLOR)

        rotate = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # cv2.imshow("img", image)

        
        try:
            frames.append(rotate.tolist())
            image_size = 0
            frame_count += 1
        except:
            conn.close()
            continue

        # cv2.imwrite(f'{frame_count}.jpg', rotate)

        # jia ie ge frame
        
        # Send if 20 frames are collected
        if frame_count == FRAME_REQUIRED: 
            frame_count = 0
            result = frame_input(frames)

            # Clear buffer
            frames.clear()

    conn.close()