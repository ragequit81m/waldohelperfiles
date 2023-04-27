import argparse
import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
from tqdm import tqdm

PicToExtract = 15

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="path to the input video file")
args = parser.parse_args()   

# Öffne das Eingabe-Video
cap = cv2.VideoCapture(args.input_file)
print(args.input_file)

# Überprüfe, ob das Video erfolgreich geöffnet wurde
if not cap.isOpened():
    print("Fehler beim Öffnen des Videos!")
    exit()

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
print(frame_width,frame_height,fps)

# Bestimme die Anzahl der Frames
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(total_frames)
split_frames = int(total_frames/PicToExtract)
print(split_frames)

for i in tqdm(range(total_frames)):
    # Lese das nächste Frame
    ret, frame = cap.read()    
    # Beende die Schleife, wenn das Video zu Ende ist
    if not ret:
        break    
    if i % split_frames == 0:            #modulos every x frames
        cv2.imwrite((str(i)+"test.jpg"), frame)
        #print('saved')   
     