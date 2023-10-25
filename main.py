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
# global Command_Recorder
global Emo_Frame
request_ptr = 0

def SLR_init():
    # Create dataset of the videos where landmarks have not been extracted yet
    # videos = load_dataset()
    # print("Done: load_dataset")

    # Create a DataFrame of reference signs (name: str, model: SignModel, distance: int)
    # reference_signs = load_reference_signs()
    global Sign_Recorder
    # global Command_Recorder
    try:
        with open("reference_signs.pickle", "rb") as file:
            loaded_reference_signs = pickle.load(file)
            Sign_Recorder = SignRecorder(loaded_reference_signs)
    except:
        reference_signs = load_reference_signs()
        Sign_Recorder = SignRecorder(reference_signs)
    # TODO: Add Command mode
    # try:
    #     with open("command_reference_signs.pickle", "rb") as file:
    #         loaded_command_signs = pickle.load(file)
    #         Command_Recorder = SignRecorder(loaded_command_signs)
            
    # except:
    #     reference_signs = load_reference_signs()
    #     Command_Recorder = SignRecorder(reference_signs)
     
        
    # Object that stores mediapipe results and computes sign similarities
    print("Done: init SignRecorder")
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
            image, results = mediapipe_detection(frame, holistic)

            # Process results
            sign_update, is_recording = sign_recorder.process_results(results)

            # Update the frame (draw landmarks & display result)
            webcam_manager.update(frame, results, str(sign_update), is_recording)
            
            counting += 1
            if counting >= 20:
                sign_recorder.record()
                counting = 0
            pressedKey = cv2.waitKey(1) & 0xFF
            
            if pressedKey == ord("q"):  # Break pressing q
                break
            
        cap.release()
        cv2.destroyAllWindows()
        print("=== END ===")
        
    
def frame_input(frame):
    global Sign_Recorder
    # Object that draws keypoints & displays results
    # Set up the Mediapipe environment
    with mediapipe.solutions.holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic:
        # Make detections
        global Emo_Frame
        Emo_Frame = []
        for i, f in enumerate(frame):
            image_array = np.array(f, dtype=np.uint8)
            image, results = mediapipe_detection(image_array, holistic)
            Sign_Recorder.process_results(results)
            if i > 5  and i < 15 and Sign_Recorder.counting == 0:
                Emo_Frame.append(f)
        Sign_Recorder.record() 
    
def emo_gpt_result():
    global Sign_Recorder
    global Emo_Frame
    if len(Sign_Recorder.detect_signs_list) > 0:
        emo_text = ""
        try:
            for emo in Emo_Frame:
                emo_text = detect_emotion(emo)
                if emo_text != "":
                    break
        except:
            pass
        if emo_text != "":
            Sign_Recorder.detect_signs_list.append(emo_text)
        GPT_Result = GPTtranslate(Sign_Recorder.detect_signs_list, c.GPT_KEY)
        print("GPT_Result:", GPT_Result)
        return GPT_Result
    else:
        print("no input")
        return "錯誤：請再次輸入"
    
def detect_result(request_ptr, gpt=False):
    result = ""
    if gpt:
        request_ptr = 0
        result = "@"
        result += emo_gpt_result()
        return result
    
    elif len(Sign_Recorder.detect_signs_list) > 0:
        if request_ptr >= len(Sign_Recorder.detect_signs_list):
            return ""
        result = Sign_Recorder.detect_signs_list[request_ptr]
        print("list= ", Sign_Recorder.detect_signs_list)

    return result
