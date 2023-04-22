
"""
findKillcam_WZ1.py

input WZ replay datei 1080
extrahiert die killcam und speichert sie in eine outputfile

findKillcam_WZ1.py
Usage: findKillcam_WZ1{Input File} 

Takes in an input video file and finds killscams based on pixel´s

Video file must be 1920 x 1080 @ 60FPS or bigger
Video should contain gameplay of WZ1
450 frame aka 7.5 seconds will be saved
"""

import argparse
import cv2
from tqdm import tqdm

def scan_red_pixel(frame_now, x, y):
    # Lese die Farbe des Pixels an der Position (x, y)
    color = frame_now[y, x]
    # Überprüfe, ob die Farbe des Pixels rot ist
    if color[0] < 120 and color[1] < 120 and color[2] > 150:
        #print ("RED Found")
        return True
    else:
        #print ("NO RED Found")
        return False
                
def scan_white_pixel(frame_now, x, y):
    # Lese die Farbe des Pixels an der Position (x, y)
    color = frame_now[y, x]
    # Überprüfe, ob die Farbe des Pixels weiss oder grau ist
    if color[0] > 230 and color[1] > 230 and color[2] > 230:
        #print ("white Found")
        return True
    else:
        #print ("NO white Found")
        return False
        
def scan_grey_pixel(frame_now, x, y):
    # Lese die Farbe des Pixels an der Position (x, y)
    color = frame_now[y, x]
    # Überprüfe, ob die Farbe des Pixels weiss oder grau ist
    if color[0] > 190 and color[1] > 190 and color[2] > 190:
        #print ("white Found")
        return True
    else:
        #print ("NO white Found")
        return False
                
        
def show_pixel_color(frame_now, x, y):
    # Lese die Farbe des Pixels an der Position (x, y)
    color = frame_now[y, x]
    # Pixelfarbe ausgeben z.b. weiss oder grau ist
    print("X:" + str(x) +" Y:" + str(y) +" B:" + str(color[0]) +" R:" + str(color[1]) +" G:" + str(color[2]))
        

        
        
      
      
parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="path to the input video file")
args = parser.parse_args()        
       
# Pfad zur Ausgabe-Video-Datei
output_video_path = "o_" + args.input_file.split("/")[-1].split(".")[0] + "_" + ".mp4"

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
#out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
found_red_pixel = False
savefile = False
startframe = 0
endframe = 0

print("frame_height: " + str(frame_height) + "  ")
if frame_height == 1080:
    coord1 = (120,188)
    coord2 = (944,700)
    coord3 = (1821,847)
elif frame_height == 1440:
    coord1 = (160,251)
    coord2 = (1258,936)
    coord3 = (2426,1129)
else:
    printprint("frame_height: " + str(frame_height) + "  != 1080 or 1440 exiting")
    exit()


for i in tqdm(range(total_frames)):
    # Lese das nächste Frame
    ret, frame = cap.read()    
    # Beende die Schleife, wenn das Video zu Ende ist
    if not ret:
        break
 

    if i > endframe and scan_red_pixel(frame, coord1[0], coord1[1]) and scan_white_pixel(frame, coord2[0], coord2[1]) and scan_grey_pixel(frame, coord3[0], coord3[1]):   #1080 and 1440   
    #if i > endframe and scan_red_pixel(frame, 120, 188) and scan_white_pixel(frame, 944, 700) and scan_grey_pixel(frame, 1821, 847):   #1080 
    #if i > endframe and scan_red_pixel(frame, 160, 251) and scan_white_pixel(frame, 1258, 936) and scan_grey_pixel(frame, 2426, 1129): #1440
    
        # startframe gefunden
        startframe = i
        endframe = i+450
        savefile = True
        print("Startframe gefunden:" + str(startframe))     
        #show_pixel_color(frame, coord1[0], coord1[1])
        #show_pixel_color(frame, coord2[0], coord2[1])
        #show_pixel_color(frame, coord3[0], coord3[1])
        
        if out is not None:
            out.release()  # Falls ein altes VideoWriter-Objekt existiert, freigegeben
        out = cv2.VideoWriter(str(startframe)+ "-" + str(endframe) + (output_video_path), fourcc, fps, (1920, 1080))
        
    if i == endframe:
        savefile = False
        if out is not None:
            out.release()
        out = None
              
    if savefile == True:
        if frame_height != 1080:
            frame = cv2.resize(frame, (1920, 1080),interpolation=cv2.INTER_AREA)
        out.write(frame)
       
cap.release()   # Schließe die Capture-Datei
if out is not None: out.release()   # Schließe die Video-Datei
        