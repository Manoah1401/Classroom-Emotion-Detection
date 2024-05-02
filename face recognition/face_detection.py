import cv2
import numpy as np
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import json

model = load_model('face_recognition_vgg16_model_1.h5')

class_names = {0: 'Jeswin', 1: 'Joshua', 2: 'Manoah', 3: 'Nikhil', 4: 'Rovin'}

emotions_occurrences = {}

main_directory = 'parent'

for subdir in os.listdir(main_directory):
    subdir_path = os.path.join(main_directory, subdir)
    if os.path.isdir(subdir_path):  
        emotions_occurrences[subdir] = {'Jeswin': 0, 'Joshua': 0, 'Manoah': 0, 'Nikhil': 0, 'Rovin': 0}
        
        for filename in os.listdir(subdir_path):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):  
                img_path = os.path.join(subdir_path, filename)
                img = cv2.imread(img_path)
                if img is not None:
                    img_resized = cv2.resize(img, (224, 224))
                    img_array = image.img_to_array(img_resized)
                    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
                    img_preprocessed = img_array_expanded_dims / 255.  

                    prediction = model.predict(img_preprocessed)
                    predicted_class_index = np.argmax(prediction, axis=1)[0]
                    predicted_class_name = class_names[predicted_class_index]

                    emotions_occurrences[subdir][predicted_class_name] += 1

print("Total occurrences per emotion in the directory:", emotions_occurrences)

with open('emotion_occurrences.json', 'w') as json_file:
    json.dump(emotions_occurrences, json_file, indent=4)
