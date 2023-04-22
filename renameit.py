import os
path = "C:/keras/ucf101top5/WZ/rename1"
files = os.listdir(path)
i = 0
j= 1
   
for index, file in enumerate(files):
    if i <=5:
        i = i+1
    else:
        i = 1
        j = j+1        
    string = "v_WZ_g0%s_C0%s.mp4" % (j , i)
    print (string)
    os.rename(os.path.join(path, file), os.path.join(path, string))