import cv2
import mediapipe
from utils.dataset_utils import load_dataset, load_reference_signs
from utils.mediapipe_utils import mediapipe_detection
from sign_recorder import SignRecorder
from webcam_manager import WebcamManager
# from emotion_detector import detect_emotion

if __name__ == "__main__":
    # Create dataset of the videos where landmarks have not been extracted yet
    videos = load_dataset()
    print("Done: load_dataset")

    # Create a DataFrame of reference signs (name: str, model: SignModel, distance: int)
    reference_signs = load_reference_signs(videos)
    print("Done: load_reference_signs")
    
    # Object that stores mediapipe results and computes sign similarities
    sign_recorder = SignRecorder(reference_signs)
    print("Done: init SignRecorder")
    
    # Object that draws keypoints & displays results
    webcam_manager = WebcamManager()

    # Turn on the webcam
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # Set up the Mediapipe environment
    with mediapipe.solutions.holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic:
        while cap.isOpened():
            # Read feed
            ret, frame = cap.read()

            ###### Test detect_emotion(frame) #######
            # emotions, emo_result, emo_value = detect_emotion(frame)
            # print(emotions)
            # print(emo_result, emo_value)
            # exit(1)

            # Make detections
            image, results = mediapipe_detection(frame, holistic)

            # Process results
            sign_detected, is_recording = sign_recorder.process_results(results)

            # Update the frame (draw landmarks & display result)
            webcam_manager.update(frame, results, sign_detected, is_recording)
            
            sign_recorder.record()
            pressedKey = cv2.waitKey(1) & 0xFF
            if pressedKey == ord("r"):  # Record pressing r
                sign_recorder.record()
                print("sign_detected", sign_detected)
            elif pressedKey == ord("q"):  # Break pressing q
                break

        cap.release()
        cv2.destroyAllWindows()
