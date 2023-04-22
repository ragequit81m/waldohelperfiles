import tensorflow as tf
import cv2
import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv3D, MaxPooling3D, Flatten, Dense
from sklearn.model_selection import train_test_split



def read_vid(videos_folder, lbl):
    # Initialize the input and label arrays
    videos = []
    labels = [] 
    #Load the video files
    videos_list = os.listdir(videos_folder)

    # Loop through all learn_videos and extract the frames
    for video in videos_list:
        print(video)
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
train_videos,train_labels = read_vid("D:/_Videos_/_train/", 1)
val_videos, val_labels = read_vid("D:/_Videos_/_val/", 1)
test_videos, test_labels = read_vid("D:/_Videos_/_test/", 1)
print("Videos read")

# Create the model
model = Sequential([
    Conv3D(32, (3, 3, 3), activation='relu', input_shape=train_videos.shape[1:]),
    MaxPooling3D((2, 2, 2)),
    Conv3D(64, (3, 3, 3), activation='relu'),
    MaxPooling3D((2, 2, 2)),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(num_classes, activation='softmax')
])

print("model created")
# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
print("model compiled")




# Separate the test data
train_videos_split, train_videos_test, train_labels_split, train_labels_test = train_test_split(train_videos, train_labels, test_size=0.20, shuffle=True)
# Split the remaining data to train and validation
#x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.15, shuffle=True)
# Training the Keras model
model.fit(x=train_videos_split, y=train_labels_split, batch_size=32, epochs=10, validation_data=(train_videos_test, train_labels_test))

# Train the model
#model.fit(train_videos, train_labels, batch_size=batch_size, epochs=no_epochs, verbose=verbosity, validation_split=validation_split,validation_data = val_videos, workers=2, use_multiprocessing=True)
#model.fit(train_videos, train_labels, batch_size=batch_size, epochs=no_epochs, verbose=verbosity, validation_split=validation_split, validation_data=(val_videos, val_labels), workers=2, use_multiprocessing=True)
print("model fitted")
model.evaluate(val_videos, return_dict=True)
print("model evaluated")
print("All done")
model.summary()

predictions = model.predict(test_videos, verbose=2,batch_size=32)
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


model.save('testmodel22.h5')




