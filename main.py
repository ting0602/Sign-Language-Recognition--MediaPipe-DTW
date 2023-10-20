import cv2
import mediapipe
from utils.dataset_utils import load_dataset, load_reference_signs
from utils.mediapipe_utils import mediapipe_detection
from webcam_manager import WebcamManager
from sign_recorder import SignRecorder
from gpt.gpt import GPTtranslate, readFile
import numpy as np
import pickle
# from emotion_detector import detect_emotion

global Sign_Recorder

def SLR_init():
    # Create dataset of the videos where landmarks have not been extracted yet
    # videos = load_dataset()
    # print("Done: load_dataset")

    # Create a DataFrame of reference signs (name: str, model: SignModel, distance: int)
    # reference_signs = load_reference_signs()
    global Sign_Recorder
    try:
        with open("reference_signs.pickle", "rb") as file:
            loaded_reference_signs = pickle.load(file)
            Sign_Recorder = SignRecorder(loaded_reference_signs)
    except:
        reference_signs = load_reference_signs()
        Sign_Recorder = SignRecorder(reference_signs)
        
    # print("reference_signs", reference_signs)
    print("Done: load_reference_signs")

    # Object that stores mediapipe results and computes sign similarities

    
    print("Done: init SignRecorder")
    print("=== Complete Initialization ===")
    
    
def webcam_input():
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
            image, results = mediapipe_detection(frame, holistic)

            # Process results
            sign_detected, is_recording = sign_recorder.process_results(results)

            # Update the frame (draw landmarks & display result)
            webcam_manager.update(frame, results, sign_detected, is_recording)
    
            # TODO: Always record
            sign_recorder.record()
            pressedKey = cv2.waitKey(1) & 0xFF
            if pressedKey == ord("r"):  # Record pressing r
                sign_recorder.record()
                print("sign_detected", sign_detected)
            elif pressedKey == ord("q"):  # Break pressing q
                break
            
        cap.release()
        cv2.destroyAllWindows()
        print(sign_recorder.detect_signs_list)

def frame_input(frame):
    global Sign_Recorder
    sign_recorder = Sign_Recorder
    
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
            sign_detected, is_recording = sign_recorder.process_results(results)
        
        # frame = cv2.imdecode(np.frombuffer(frame, np.uint8), cv2.IMREAD_COLOR)
        # print("new:", frame)
        # try:

        # except:
        #     print("ERROR")
        # Process results
            # sign_detected, is_recording = sign_recorder.process_results(results)
        # TODO: Always record
        sign_recorder.record()

        # Update the frame (draw landmarks & display result)
        # webcam_manager.update(frame, results, sign_detected, is_recording)


        # if pressedKey == ord("r"):  # Record pressing r
        #     sign_recorder.record()
        #     print("sign_detected", sign_detected)
        # elif pressedKey == ord("q"):  # Break pressing q
        #     break

    return sign_recorder.stop_input    
    # print(sign_recorder.detect_signs_list)
    # return sign_recorder.detect_signs_list

def detect_result():
    Question = Sign_Recorder.detect_signs_list
    
    # key = readFile("key.txt")
    # result = GPTtranslate(Question, key)
    # print(' '.join(Question))
    # print(result)
    result = ""
    if Sign_Recorder.stop_input:
        result = "輸入完成，這是測試用回覆句!"
    elif len(Sign_Recorder.detect_signs_list) > 0:
        result = Sign_Recorder.detect_signs_list[-1]

    return result
    # with open('output.txt', 'w', encoding='utf-8') as output_file:
    #     output_file.write(result)