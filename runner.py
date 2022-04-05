import os
import subprocess
import numpy as np
import pandas as pd
import cv2
from os.path import isfile,join
from tqdm import tqdm
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
  for dir in tqdm(os.listdir('/home/haov/class_action')):
      pathIn= '/home/haov/class_action/{}/'.format(dir)
      pathOut = '/home/haov/action_rec/videos/{}.avi'.format(dir)
      fps = 1.0
      convert_frames_to_video(pathIn, pathOut, fps)


def train():
  res_txt = np.asarray([])
  index = 0
  for video in tqdm(os.listdir('./videos')):
    index += 1
    if index is 2:
      break
    name = video.replace('.avi','')
    # print(video)
    # break
    run = subprocess.run(f'python3 main.py --video {path}/videos/{video} --name {name}',shell = True)
    print(run)

    txt = np.array([])
    print('--------------------------------')
    with open(str(path) + '/out_txt/' + str(name)  + '.txt','r') as f:
      lines = f.readlines()
      for i in range(len(lines)):
        lines[i] = lines[i].replace('\n','')
        lines[i] = lines[i].split(' ')
        lines[i] = lines[i][:36]
        try:
          lines[i].remove('')
        except ValueError:
          pass
        lines[i] = np.array([float(x) for x in lines[i]])
       

      
      lines = [x for x in lines if len(x) is not 0 ]
      txt = np.stack(lines).astype(None)
      
      print(txt.shape)
      cl =  np.full((txt.shape[0],1), float(name))
      txt = np.concatenate((txt,cl), axis = 1)
      if len(res_txt):
        res_txt = np.concatenate((txt,res_txt), axis = 0)
      else:
        res_txt = txt
    # chua biet cach add ra sau cung`
  np.savetxt(str(path) + '/out_txt/res.txt', res_txt, delimiter=',',fmt='%1.4e')
  convert_to_txt = pd.read_csv(str(path) + '/out_txt/res.txt')
  convert_to_txt.to_csv (str(path) + '/Action/training/train_csv_file/' +'res.csv' , index=None)

create_video()
train()


  
