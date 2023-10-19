import requests
import json
import numpy as np
import cv2

global FramesBuffer
global ResultText
frame_len = 20
server_url = "https://3353-2001-288-4001-d889-942b-bf46-ec15-9bb2.ngrok-free.app"

def init_slr():
    init_url = f"{server_url}/api/init"
    response = requests.post(init_url)
    global FramesBuffer, ResultText
    FramesBuffer = []
    ResultText = ""
    if response.status_code == 200:
        # json.loads(response.text)["message"]
        print("DONE: SLR Init")
    else:
        print("Fail: SLR Init")

def send_frame(frame_data):
    # frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
    global FramesBuffer, ResultText
    if len(FramesBuffer) < 20:
        # frame_data = list(frame_data)
        FramesBuffer.append(frame_data.tolist())
        # FramesBuffer.append(frame_data)
        print("append")
        return False
    else:
        slr_url = f"{server_url}/api/slr"
        data_to_send = {'frames': FramesBuffer}
        headers = {'Content-type': 'application/json'}
        response = requests.post(slr_url, data=json.dumps(data_to_send), headers=headers)
        # response = requests.post(slr_url, data=data_to_send)
        FramesBuffer = []
        if response.status_code == 200:
            global ResultText
            res = json.loads(response.text)
            ResultText = res["message"]
            is_stop = res["bool"]
            print("return TEXT:", ResultText)
            return is_stop
        else:
            print("ERROR")
            return True

def get_text():
    global ResultText
    return ResultText


def get_text():
    global ResultText
    return ResultText

init_slr()
arr = [1,2,3], [4,5,6], [224,225,26]
for i in range(21):
    send_frame(np.array(arr))