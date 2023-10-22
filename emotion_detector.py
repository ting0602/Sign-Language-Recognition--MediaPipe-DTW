import config as c
import base64
from googleapiclient import discovery
import cv2
import numpy as np

def get_vision_service():
    return discovery.build('vision', 'v1', developerKey=c.API_KEY)

def detect_emotion(face_file, max_results=4, type=1):
    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )
    likelihood_mapping = {name: idx for idx, name in enumerate(likelihood_name)}
    
    
    # Input: Frame
    # Convert the frame to JPEG format
    if type:
        _, encoded_image = cv2.imencode(".jpg", face_file)

        # Ensure that encoded_image is of type bytes
        if isinstance(encoded_image, np.ndarray):
            encoded_image = encoded_image.tobytes()

        # Ensure image_content is bytes
        image_content = encoded_image

    # Input: file
    else:
        image_content = face_file.read()
    
    batch_request = [{
        'image': {
            'content': base64.b64encode(image_content).decode('utf-8')
            },
        'features': [{
            'type': 'FACE_DETECTION',
            'maxResults': max_results,
            }]
        }]

    service = get_vision_service()
    request = service.images().annotate(body={
        'requests': batch_request,
        })
    response = request.execute()

    face_annotations = response['responses'][0]['faceAnnotations']

    emotions = []
    for annotation in face_annotations:
        emotion = {
            'joyLikelihood': likelihood_mapping.get(annotation.get('joyLikelihood', 'UNKNOWN'), 0),
            'sorrowLikelihood': likelihood_mapping.get(annotation.get('sorrowLikelihood', 'UNKNOWN'), 0),
            'angerLikelihood': likelihood_mapping.get(annotation.get('angerLikelihood', 'UNKNOWN'), 0),
            'surpriseLikelihood': likelihood_mapping.get(annotation.get('surpriseLikelihood', 'UNKNOWN'), 0),
        }
        emotions.append(emotion)

    # Find the emotion with the highest value
    # max_emotion = max(emotions, key=lambda e: max(e.values()))

    # Create the second and third values as specified
    # emo_value = max(max_emotion.values())  # The highest value

    # emotion_names = list(likelihood_mapping.keys())
    # emotion_index = list(max_emotion.values()).index(emo_value)
    # emo_result = emotion_names[emotion_index]
    # emo_value = max(max_emotion.values())
    
    
    emotion_text = ""
    print("emo:", emotions)
    if emotions[0]["joyLikelihood"] >= 3:
        emotion_text = "~"
    if emotions[0]["surpriseLikelihood"] >= 3:
        emotion_text = "？"
    # print(emotions, emo_result, emo_value)
    return emotion_text
    # return emotions, emo_result, emo_value

######## Test detect_emotion(file) ########
# with open('./what.png', 'rb') as face_file:
#     text = detect_emotion(face_file, type=0)
#     print(text)