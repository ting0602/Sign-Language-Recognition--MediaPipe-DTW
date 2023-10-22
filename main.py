import cv2
import mediapipe
from utils.dataset_utils import load_dataset, load_reference_signs
from utils.mediapipe_utils import mediapipe_detection
from webcam_manager import WebcamManager
from sign_recorder import SignRecorder
from gpt.gpt import GPTtranslate, readFile
import numpy as np
import pickle
from emotion_detector import detect_emotion
import config as c

global Sign_Recorder
global Command_Recorder
global GPT_Result
GPT_Result = ""
request_ptr = 0

def SLR_init():
    # Create dataset of the videos where landmarks have not been extracted yet
    # videos = load_dataset()
    # print("Done: load_dataset")

    # Create a DataFrame of reference signs (name: str, model: SignModel, distance: int)
    # reference_signs = load_reference_signs()
    global Sign_Recorder
    global Command_Recorder
    try:
        with open("reference_signs.pickle", "rb") as file:
            loaded_reference_signs = pickle.load(file)
            Sign_Recorder = SignRecorder(loaded_reference_signs)
    except:
        reference_signs = load_reference_signs()
        Sign_Recorder = SignRecorder(reference_signs)
    try:
        with open("command_reference_signs.pickle", "rb") as file:
            loaded_command_signs = pickle.load(file)
            Command_Recorder = SignRecorder(loaded_command_signs)
            
    except:
        reference_signs = load_reference_signs()
        Command_Recorder = SignRecorder(reference_signs)
        
    # Object that stores mediapipe results and computes sign similarities

    
    print("Done: init SignRecorder")
    print("Done: init Command_Recoder")
    print("=== Complete Initialization ===")
    
def webcam_input():
    counting = 0
    global Sign_Recorder
    print(Sign_Recorder)
    sign_recorder = Sign_Recorder
    # Object that draws keypoints & displays results
    webcam_manager = WebcamManager()

    # Turn on the webcam
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # Set up the Mediapipe environment
    with mediapipe.solutions.holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic:
        cap.isOpened()
        # while cap.isOpened():
        while not sign_recorder.stop_input:
            # Read feed
            ret, frame = cap.read()
                ###### Test detect_emotion(frame) #######
                # emotions, emo_result, emo_value = detect_emotion(frame)
                # print(emotions)
                # print(emo_result, emo_value)
                # exit(1)
                ########################################

                # Make detections
            # FIXME: input: gray
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
                # frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
                # print(gray.shape, frame.shape)
            image, results = mediapipe_detection(frame, holistic)

            # Process results
            sign_detected, is_recording = sign_recorder.process_results(results)
            
            # FIXME: input: gray
            # frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            
            
            # Update the frame (draw landmarks & display result)
            webcam_manager.update(frame, results, sign_detected, is_recording)
            
            counting += 1
            if counting >= 20:
                sign_recorder.record()
                counting = 0
            pressedKey = cv2.waitKey(1) & 0xFF
            if pressedKey == ord("r"):  # Record pressing r
                # sign_recorder.record()
                print("sign_detected", sign_detected)
            elif pressedKey == ord("q"):  # Break pressing q
                break
            
        cap.release()
        cv2.destroyAllWindows()
        print("=== END ===")
        if len(sign_recorder.detect_signs_list) > 0:
            print("face frame", sign_recorder.face_frame.shape)
            print("face frame", sign_recorder.face_frame)
            emo_text = detect_emotion(sign_recorder.face_frame)
            print(sign_recorder.detect_signs_list)
            if emo_text != "":
                sign_recorder.detect_signs_list.append(emo_text)
            # TODO: gpt
            global GPT_Result
            GPT_Result = GPTtranslate(sign_recorder.detect_signs_list, c.GPT_KEY)
            print("GPT_Result:", GPT_Result)
        else:
            print("no input")
        
    
def frame_input(frame):
    global Sign_Recorder
    # sign_recorder = Sign_Recorder
    
    # Object that draws keypoints & displays results
    # webcam_manager = WebcamManager()
    

    # Set up the Mediapipe environment
    with mediapipe.solutions.holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic:
        # while not sign_recorder.stop_input:
        
        ###### Test detect_emotion(frame) #######
        # emotions, emo_result, emo_value = detect_emotion(frame)
        # print(emotions)
        # print(emo_result, emo_value)
        # exit(1)
        ########################################

        # Make detections
        # print("origin shape:", frame.shape)
        # frames_list = []
        for i, f in enumerate(frame):
            # frame_data_bytes = bytes(f)
            image_array = np.array(f, dtype=np.uint8)
            # print(image_array.shape)
            # frames_list.append(image_array)
            # try:
            image, results = mediapipe_detection(image_array, holistic)
            Sign_Recorder.process_results(results)
                # sign_detected, is_recording = Sign_Recorder.process_results(results)
            # except:
            #     print(f"Error: mediapipe_detection #{i}")
            #     break
        # frame = cv2.imdecode(np.frombuffer(frame, np.uint8), cv2.IMREAD_COLOR)
        
        Sign_Recorder.record()


    # return sign_recorder.stop_input    
    

# def detect_result():
#     if Sign_Recorder.is_stop:
#         return GPT_Result
    
#     result = ""
#     if len(Sign_Recorder.detect_signs_list) > 0:
#         result = Sign_Recorder.detect_signs_list[-1]

#     return result

    
def detect_result(request_ptr):
    result = ""
    if Sign_Recorder.stop_input:
        request_ptr = 0
        result = "@"
        for sl in Sign_Recorder.detect_signs_list:
            result +=  sl
        return result
    
    elif len(Sign_Recorder.detect_signs_list) > 0:
        if request_ptr >= len(Sign_Recorder.detect_signs_list):
            return ""
        result = Sign_Recorder.detect_signs_list[request_ptr]
        print("list= ", Sign_Recorder.detect_signs_list)

    return result
    
# SLR_init()
# webcam_input()