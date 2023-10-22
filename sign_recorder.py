import pandas as pd
import numpy as np
from collections import Counter

from utils.dtw import dtw_distances
from models.sign_model import SignModel
from utils.landmark_utils import extract_landmarks

global No_hand

# FIXME: seq_len
class SignRecorder(object):
    def __init__(self, reference_signs: pd.DataFrame, seq_len=15):
        # Variables for recording
        self.is_recording = False
        self.seq_len = seq_len

        # List of results stored each frame
        self.recorded_results = []

        # DataFrame storing the distances between the recorded sign & all the reference signs from the dataset
        self.reference_signs = reference_signs
        
        self.detect_sign = ""
        
        self.last_sign = ""
        
        self.counting = 0
        
        self.detect_signs_list = []
        
        self.stop_input = False
        
        self.face_frame = np.empty([1])

        global No_hand
        No_hand = False

    def record(self):
        """
        Initialize sign_distances & start recording
        """
        try:
            self.reference_signs["distance"].values[:] = 0
            self.is_recording = True
        except:
            pass

    def process_results(self, results) -> (str, bool):
        """
        If the SignRecorder is in the recording state:
            it stores the landmarks during seq_len frames and then computes the sign distances
        :param results: mediapipe output
        :return: Return the word predicted (blank text if there is no distances)
                & the recording state
        """
        # if self.is_recording:
        if len(self.recorded_results) < self.seq_len:
            self.recorded_results.append(results)
        else:
            print("start detect")
            self.compute_distances()
            if No_hand: self.detect_no_hand()
            else: self._get_sign_predicted()
            self.recorded_results = []
            # pred_sign = self._get_sign_predicted()
            # self.check_sign_state()
            # if self.detect_sign != "": -> move to detect no hand
            #     self.counting = 0
            # return pred_sign, self.is_recording
                
            # no result
            # if np.sum(self.reference_signs["distance"].values) == 0 or np.sum(self.reference_signs["distance"].values) > 10000:
            #     self.detect_no_hand()
            #     return "", self.is_recording
        return "", self.is_recording

    def compute_distances(self):
        """
        Updates the distance column of the reference_signs
        and resets recording variables
        """
        No_hand = False
        left_hand_list, right_hand_list = [], []
        for results in self.recorded_results:
            # if a hand doesn't appear, return an array of zeros
            _, left_hand, right_hand = extract_landmarks(results)
            if left_hand is None: 
                No_hand = True
                break
            left_hand_list.append(left_hand)
            right_hand_list.append(right_hand)

        if No_hand:  return

        # Create a SignModel object with the landmarks gathered during recording
        recorded_sign = SignModel(left_hand_list, right_hand_list)

        # Compute sign similarity with DTW (ascending order)
        self.reference_signs = dtw_distances(recorded_sign, self.reference_signs)

        # # Reset variables
        # self.recorded_results = []
        # self.is_recording = False

    def _get_sign_predicted(self, batch_size=12, threshold=0.4):
        """
        Method that outputs the sign that appears the most in the list of closest
        reference signs, only if its proportion within the batch is greater than the threshold

        :param batch_size: Size of the batch of reference signs that will be compared to the recorded sign
        :param threshold: If the proportion of the most represented sign in the batch is greater than threshold,
                        we output the sign_name
                          If not,
                        we output "Sign not found"
        :return: The name of the predicted sign
        """
        if self.reference_signs is None:
            self.detect_sign = ""
            self.detect_no_hand()
            return

        # Get the list (of size batch_size) of the most similar reference signs
        sign_names = self.reference_signs.iloc[:batch_size]["name"].values

        # Count the occurrences of each sign and sort them by descending order
        sign_counter = Counter(sign_names).most_common()
        print("sign names", sign_names)
        predicted_sign, count = sign_counter[0]
        print(predicted_sign, count / batch_size)
        if (count / batch_size) < threshold:
            self.detect_sign = ""
            # return self.check_sign_state()
            # self.check_sign_state()
            if (count / batch_size) < 0.3:
                self.detect_no_hand()
            # return ""
        else:
            self.counting = 0
            self.detect_sign = predicted_sign
            self.check_sign_state()
            print("predict:", predicted_sign)
            # self.face_frame = self.recorded_results[10]
            
        # return self.detect_sign
        # return self.check_sign_state()

    def check_sign_state(self):
        if self.detect_sign != self.last_sign and self.detect_sign != "":
            self.detect_signs_list.append(self.detect_sign)
            self.last_sign = self.detect_sign
            # return False
        else: self.is_recording = True
        # return True
    
    def detect_no_hand(self):
        self.counting += 1
        print("no!")
        if self.counting > 3:
            print("STOP!")
            # self.is_recording = False
            self.stop_input = True