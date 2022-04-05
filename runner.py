import os
import subprocess
import numpy as np
import pandas as pd
import cv2
from os.path import isfile,join
path = os.path.abspath(os.getcwd())


def convert_frames_to_video(pathIn,pathOut,fps):
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
    #for sorting the file names properly
    # files.sort(key = lambda x: int(x[5:-4]))
    for i in range(len(files)):
        filename=pathIn + files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        print(filename)
        #inserting the frames into an image array
        frame_array.append(img)
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()

def create_video():
  for dir in os.listdir('/home/haov/class_action'):
      pathIn= '/home/haov/class_action/{}/'.format(dir)
      pathOut = '/home/haov/action_rec/videos/{}.avi'.format(dir)
      fps = 1.0
      convert_frames_to_video(pathIn, pathOut, fps)


def train():
  res_txt = np.array([])
  for video in os.listdir('./videos'):
    name = video.replace('.mp4','')
    print(video)
    # break
    run = subprocess.run(f'python main.py --video {path}/videos/{video} --name {name}',shell = True)
    print(run)
    txt = np.genfromtxt(str(path) + '/out_txt/' + str(name)  + '.txt')
    cl =  np.full((txt.shape[0],1), name)
    txt = np.concatenate((txt,cl), axis = 1)
    # chua biet cach add ra sau cung`
    res_txt.append(txt)
  np.savetxt(str(path) + '/out_txt/res.txt', res_txt, delimiter=',',fmt='%1.4e')
  convert_to_txt = pd.read_csv(str(path) + '/out_txt/res.txt')
  convert_to_txt.to_csv (str(path) + '/training/train_csv_file/' + f'{name}.csv' , index=None)

create_video()
train()
<<<<<<< HEAD

=======
>>>>>>> 285c01cfde1f1140084617884a0ace7e557962bf


  
