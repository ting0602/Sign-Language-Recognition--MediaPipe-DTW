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
global frame_counting
global times
global face_frame
times = 0
frame_counting = 0
GPT_Result = ""

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
    # sign_recorder = Sign_Recorder
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
        while not Sign_Recorder.stop_input:
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
            Sign_Recorder.process_results(results)
            
            # FIXME: input: gray
            # frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            
            
            # Update the frame (draw landmarks & display result)
            webcam_manager.update(frame, results, "", True)
            
            counting += 1
            if counting >= 20:
                Sign_Recorder.record()
                counting = 0
            pressedKey = cv2.waitKey(1) & 0xFF
            if pressedKey == ord("r"):  # Record pressing r
                # sign_recorder.record()
                print("sign_detected", Sign_Recorder)
            elif pressedKey == ord("q"):  # Break pressing q
                break
            
        cap.release()
        cv2.destroyAllWindows()
        print("=== END ===")
        # if len(Sign_Recorder.detect_signs_list) > 0:
        #     print("face frame", Sign_Recorder.face_frame)
        #     emo_text = detect_emotion(Sign_Recorder.face_frame)
        #     print(Sign_Recorder.detect_signs_list)
        #     if emo_text != "":
        #         Sign_Recorder.detect_signs_list.append(emo_text)
        #     # TODO: gpt
        #     global GPT_Result
        #     GPT_Result = GPTtranslate(Sign_Recorder.detect_signs_list, c.GPT_KEY)
        #     print("GPT_Result:", GPT_Result)
        # else:
        #     print("no input")
    
def frame_input(frame):
    global Sign_Recorder
    
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
        for f in frame:
            # frame_data_bytes = bytes(f)
            image_array = np.array(f, dtype=np.uint8)
            print(image_array.shape)
            # frames_list.append(image_array)
            image, results = mediapipe_detection(image_array, holistic)
            Sign_Recorder.process_results(results)
        
        # frame = cv2.imdecode(np.frombuffer(frame, np.uint8), cv2.IMREAD_COLOR)
        
        Sign_Recorder.record()

def single_frame_input(frame):
    global Sign_Recorder
    
    # Object that draws keypoints & displays results
    # webcam_manager = WebcamManager()
    
    global frame_counting
    global times
    # Set up the Mediapipe environment
    with mediapipe.solutions.holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic:

        # frame_data_bytes = bytes(f)
        image_array = np.array(frame, dtype=np.uint8)
        # print(image_array.shape)
        # frames_list.append(image_array)
        try:
            image, results = mediapipe_detection(image_array, holistic)
            print("OK: detect hand")
            Sign_Recorder.process_results(results)
            print("res arr:", len(Sign_Recorder.recorded_results))
            frame_counting += 1
            times = 0
            print("frame pass~~~~", frame_counting)
        except:
            print("frame error", frame_counting)
            times += 1

        if frame_counting > 20:
            frame_counting = 0
            Sign_Recorder.record()
            Sign_Recorder.recorded_results = []
        # if times > 10:
        #     print("no hands -- stop detect")
        #     Sign_Recorder.stop_input = True
        #     detect_result()
    
# def emo_gpt_result():
#     global Sign_Recorder
#     if len(Sign_Recorder.detect_signs_list) > 0:
#         print("face frame", Sign_Recorder.face_frame)
#         emo_text = detect_emotion(Sign_Recorder.face_frame)
#         print(Sign_Recorder.detect_signs_list)
#         if emo_text != "":
#             Sign_Recorder.detect_signs_list.append(emo_text)
#         # TODO: gpt
#         global GPT_Result
#         GPT_Result = GPTtranslate(Sign_Recorder.detect_signs_list, c.GPT_KEY)
#         print("GPT_Result:", GPT_Result)
#     else:
#         print("no input")
    
def detect_result():
    global Sign_Recorder
    result = ""
    if Sign_Recorder.stop_input:
        result = "@"
        for sl in Sign_Recorder.detect_signs_list:
            result +=  sl
        return result
    
    elif len(Sign_Recorder.detect_signs_list) > 0:
        result = Sign_Recorder.detect_signs_list[-1]

    return result
    
# SLR_init()
# webcam_input()