import os
import sys
from moviepy.editor import VideoFileClip 
from moviepy.video.fx import rotate

def rotate_video(dir, in_angle, name_end):
    for root, dirs, files in os.walk(dir):
        for dir in dirs:
            rotate_video(dir, in_angle, name_end)
        for file in files:
            in_path = os.path.join(root, file)
            in_name, in_ext = os.path.splitext(file)
            if in_path.lower().endswith(".mp4") and in_name.find('rotate')==-1:
                clip = VideoFileClip(in_path)
                output = clip.rotate(in_angle)
                
                out_name = os.path.join(root, f'{in_name}-{name_end}{in_ext}')
                output.write_videofile(out_name)

if __name__ == '__main__':
    dir_name = sys.argv[1]
    
    #you can modify or add new speed
    name_end= ['rotate1', 'rotate2']
    rotate_video(dir_name, 15, name_end[0])
    rotate_video(dir_name, -15, name_end[1])
    

