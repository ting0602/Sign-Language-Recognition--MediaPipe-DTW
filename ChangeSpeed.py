import os
import sys
from moviepy.editor import VideoFileClip 


def change_speed(dir, speed, name_end):
    for root, dirs, files in os.walk(dir):
        for dir in dirs:
            change_speed(dir, speed, name_end)
        for file in files:
            in_path = os.path.join(root, file)
            in_name, in_ext = os.path.splitext(file)
            if in_path.lower().endswith(".mp4") and in_name.find('speed')==-1:
                clip = VideoFileClip(in_path)
                output = clip.speedx(speed)
                
                out_name = os.path.join(root, f'{in_name}-{name_end}{in_ext}')
                output.write_videofile(out_name)

if __name__ == '__main__':
    dir_name = sys.argv[1]
    
    #you can modify or add new speed
    name_end= ['speed1', 'speed2']
    change_speed(dir_name, 1.5, name_end[0])
    change_speed(dir_name, 0.7, name_end[1])
    

