import tensorflow as tf
import cv2
import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv3D, MaxPooling3D, Flatten, Dense



def read_vid(videos_folder, lbl):
    # Initialize the input and label arrays
    videos = []
    labels = [] 
    #Load the video files
    videos_list = os.listdir(videos_folder)

    # Loop through all learn_videos and extract the frames
    for video in videos_list:
        # Load the video
        video_path = os.path.join(videos_folder, video)
        cap = cv2.VideoCapture(video_path)
        frames = []
        # Loop through all frames in the video
        while True:
            ret, frame = cap.read()
            if ret:
                # Apply preprocessing to the frame (e.g. scaling)
                frame = cv2.resize(frame, frame_size)
                # Add the frame to the input array
                frames.append(frame)
            else:
                break
        # Release the video capture object
        cap.release()
        # Append the input and label arrays
        videos.append(frames)
        labels.append(lbl)     
    # Convert the videos and labels to NumPy arrays
    videos = np.array(videos, dtype=np.float32)
    labels = np.array(labels, dtype=np.int32)

    return videos, labels
  


# Model configuration
batch_size = 2
no_epochs = 5
learning_rate = 0.001
validation_split = 0.2
verbosity = 2

# Number of classes and size of input frames
num_classes = 2
frame_size = (128, 128)


train_videos = []
train_labels = []
#train_videos,train_labels = read_vid("D:/_Videos_/_train/", 1)
#val_videos, val_labels = read_vid("D:/_Videos_/_val/", 1)
test_videos, test_labels = read_vid("D:/_Videos_/_test/", 1)
print("Videos read")


model = tf.keras.models.load_model('testmodel22.h5')
model.summary()
print("Model loaded")

# Berechnen der Vorhersagen für jedes Frame
#predictions = model.predict(videos)
predictions = model.predict(test_videos, verbose=2,batch_size=batch_size,)
print(predictions)
# Train the model
#model.fit(videos, labels, batch_size=batch_size, epochs=no_epochs, validation_split=validation_split)

# Berechnen des Durchschnitts der Vorhersagen für alle Frames
average_prediction = np.mean(predictions)
# Vergleichen Sie den Durchschnitt der Vorhersagen mit einem Schwellenwert, um festzustellen, ob das Video ähnlich ist oder nicht
if average_prediction > 0.8:
    print("Das Video ist ähnlich zu den trainierten Videos.")
    print(average_prediction)
else:
    print("Das Video ist nicht ähnlich zu den trainierten Videos.")
    print(average_prediction)
print("pediction done")


# Compile the model
#model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


print("All done")

#model.evaluate((test_videos, test_labels), return_dict=True)


#model.evaluate((test_videos, test_labels), return_dict=True)