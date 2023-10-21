import os
import pandas as pd
from tqdm import tqdm
from models.sign_model import SignModel
from utils.landmark_utils import save_landmarks_from_video, load_array
import pickle

def load_dataset():
    videos = [
        # file_name.replace(".mkv", "")
        file_name.replace(".mp4", "")
        for root, dirs, files in os.walk(os.path.join("data", "videos"))
        for file_name in files
        if file_name.endswith(".mp4")
        # if file_name.endswith(".mkv")
    ]
    dataset = [
        file_name.replace(".pickle", "").replace("pose_", "")
        for root, dirs, files in os.walk(os.path.join("data", "dataset"))
        for file_name in files
        if file_name.endswith(".pickle") and file_name.startswith("pose_")
    ]
    # Create the dataset from the reference videos
    videos_not_in_dataset = list(set(videos).difference(set(dataset)))
    n = len(videos_not_in_dataset)
    if n > 0:
        print(f"\nExtracting landmarks from new videos: {n} videos detected\n")

        for idx in tqdm(range(n)):
            save_landmarks_from_video(videos_not_in_dataset[idx])
            
    with open("video_name.txt", "w", encoding="utf-8") as file:
        for video_name in videos:
            file.write(video_name + "\n")

def load_reference_signs():
    with open("video_name.txt", "r", encoding="utf-8") as file:
        videos = [line.strip() for line in file]
        
    reference_signs = {"name": [], "sign_model": [], "distance": []}
    for video_name in videos:
        sign_name = video_name.split("-")[0]
        path = os.path.join("data", "dataset", sign_name, video_name)

        left_hand_list = load_array(os.path.join(path, f"lh_{video_name}.pickle"))
        right_hand_list = load_array(os.path.join(path, f"rh_{video_name}.pickle"))

        reference_signs["name"].append(sign_name)
        reference_signs["sign_model"].append(SignModel(left_hand_list, right_hand_list))
        reference_signs["distance"].append(0)
    
    reference_signs = pd.DataFrame(reference_signs, dtype=object)
    print(
        f'Dictionary count: {reference_signs[["name", "sign_model"]].groupby(["name"]).count()}'
    )
    # Serialize and save the reference_signs to a file
    with open("reference_signs.pickle", "wb") as file:
        pickle.dump(reference_signs, file)

    # Load the reference_signs from the file

    return reference_signs    