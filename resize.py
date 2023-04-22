
"""
resize_video.py
input big *.avi
output WZ replay datei 320x240
"""
import argparse
import cv2
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="path to the input video file")
args = parser.parse_args()  
print (args)      
       
# Pfad zur Ausgabe-Video-Datei
output_video_path = "" + args.input_file.split("/")[-1].split(".")[0] + "_" + ".mp4"
print(output_video_path)

# Überprüfe, ob die Ausgabe-Datei bereits existiert
import os
if os.path.isfile(output_video_path):
    print("Die Ausgabe-Datei existiert bereits! Bitte ändern Sie den Dateinamen.")
    exit()

# Öffne das Eingabe-Video
cap = cv2.VideoCapture(args.input_file)

# Überprüfe, ob das Video erfolgreich geöffnet wurde
if not cap.isOpened():
    print("Fehler beim Öffnen des Videos!")
    exit()
    
# Lege die FourCC-Codecs für das Ausgabe-Video fest
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# Bestimme die Video-Auflösung
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
# Bestimme die Anzahl der Frames
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# Erstelle den VideoWriter für die Ausgabe-Video-Datei
out = None
out = cv2.VideoWriter(output_video_path, fourcc, fps, (320, 240))

for i in tqdm(range(total_frames)):
    # Lese das nächste Frame
    ret, frame = cap.read()    
    # Beende die Schleife, wenn das Video zu Ende ist
    if not ret:
        break
    frame = cv2.resize(frame, (320, 240),interpolation=cv2.INTER_AREA)
    out.write(frame)
       
cap.release()   # Schließe die Capture-Datei
out.release()   # Schließe die Video-Datei
        