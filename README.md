# Sign Language Recognition - using MediaPipe and DTW

## Resource

This repository proposes an implementation of a Sign Recognition Model using the **MediaPipe** library 
for landmark extraction and **Dynamic Time Warping** (DTW) as a similarity metric between signs.

#### Source : https://www.sicara.ai/blog/sign-language-recognition-using-mediapipe
___
## Introduction - Sign Input
### [2023 Meichu Hackathon](https://2023.meichuhackathon.org/)

**Company:** Google

**Ranking:** Second place

**Theme:** [Suppor&ve Phone for All People](https://2023.meichuhackathon.org/assets/pdfs/Google_2023.pdf)

**Introduction:**

We have developed an Android app called "Sign Input" (Sign Language Input Method) tailored for the deaf community in Taiwan, catering to their unique communication needs. 

This app incorporates three essential features:

**1. Word Recognition:** We employ the Mediapipe framework in conjunction with the DTW (Dynamic Time Warping) algorithm to quickly recognize individual sign language words, even with limited data.

**2. Emotion and Expression Analysis:** Leveraging the Google Cloud Vision API, we have gathered a substantial dataset of images for emotion recognition. This allows us to discern whether a sentence is a question or a statement based on the facial expressions in the communication.

**3. Grammar Enhancement:** To ensure that the sentences are in a format that is easily comprehensible to the general public, we have integrated OpenAI's GPT-3.5 model. By providing GPT with sets of example sentence structures, it rephrases and organizes the sentences into more commonly used grammatical forms.

We envision that the Sign Input app is just the beginning of our journey. We hope to expand this technology for various applications, including phone communication and real-time Google Meet subtitle translation. 

Our ultimate goal is to eliminate the barriers that deaf individuals face in their work and daily lives, allowing them to overcome their hearing impairment. Our aspiration is to bridge the communication divide, fostering a more inclusive society where everyone can connect without hindrance.

*Note: You will need the [Android-side code](https://github.com/luckyjp6/Sign-Language-Recognition) to run this application.*

**Report:** [Sign Input](https://github.com/ting0602/Sign-Language-Recognition--MediaPipe-DTW/blob/main/SignInput.pdf)

**Demo:**
![image](https://github.com/ting0602/Sign-Language-Recognition--MediaPipe-DTW/blob/main/2023mc_hackathon_demo.gif)
___
## Set up

### 1. Open terminal and go to the Project directory

### 2. Install the necessary libraries

` pip install -r requirements.txt `

### 3. Import Videos of signs which will be considered as reference
The architecture of the `videos/` folder must be:
```
|data/
    |-videos/
          |-Hello/
            |-<video_of_hello_1>.mp4
            |-<video_of_hello_2>.mp4
            ...
          |-Thanks/
            |-<video_of_thanks_1>.mp4
            |-<video_of_thanks_2>.mp4
            ...
```

To automatically create a small dataset of French signs:

- Install `ffmpeg` (for MacOS `brew install ffmpeg`)
- Run: ` python yt_download.py `
- Add more YouTube links in ``yt_links.csv`` if needed
> N.B. The current dataset is insufficient to obtain good results. Feel free to add more links or import your own videos 

### 4. Load the dataset

- ` python init_video.py `

### 5. Run server to record the sign

- ` python server_socket.py `
___
## Code Description

### *Landmark extraction (MediaPipe)*

- The **Holistic Model** of MediaPipe allows us to extract the keypoints of the Hands, Pose and Face models.
For now, the implementation only uses the Hand model to predict the sign.


### *Hand Model*

- In this project a **HandModel** has been created to define the Hand gesture at each frame. 
If a hand is not present we set all the positions to zero.

- In order to be **invariant to orientation and scale**, the **feature vector** of the
HandModel is a **list of the angles** between all the connexions of the hand.

### *Sign Model*

- The **SignModel** is created from a list of landmarks (extracted from a video)

- For each frame, we **store** the **feature vectors** of each hand.

### *Sign Recorder*

- The **SignRecorder** class **stores** the HandModels of left hand and right hand for each frame **when recording**.
- Once the recording is finished, it **computes the DTW** of the recorded sign and 
all the reference signs present in the dataset.
- Finally, a voting logic is added to output a result only if the prediction **confidence** is **higher than a threshold**.

### *Dynamic Time Warping*

-  DTW is widely used for computing time series similarity.

- In this project, we compute the DTW of the variation of hand connexion angles over time.

___

## Other Tool

### ChangeSpeed and RotateVideo Usage
ChangeSpeed.py recursively modify the video speed (can be modified in .py) and save as a new video named as {original_name-speedi}.
RotateVideo.py do the rotation of the mp4 file (the angle can be modified in .py). The output is named as {original_name-rotatei}.
default speed: 0.7, 1.5 
default angle: 15, -15
```
pip install moviepy
python ChangeSpeed.py <dir_name>
python RotateVideo.py <dir_name>
```
___

## References

 - [Pham Chinh Huu, Le Quoc Khanh, Le Thanh Ha : Human Action Recognition Using Dynamic Time Warping and Voting Algorithm](https://www.researchgate.net/publication/290440452)
 - [Mediapipe : Pose classification](https://google.github.io/mediapipe/solutions/pose_classification.html)
 - [Reference Github](https://github.com/gabguerin/Sign-Language-Recognition--MediaPipe-DTW)

