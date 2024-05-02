import cv2
import numpy as np
import os
from tensorflow.keras.models import load_model

print("[INFO] loading RAF-DB model...")
emotion_model = load_model('rafdb.h5')
print("Loaded RAF-DB model from disk")

emotion_dict = {0: "Disgust", 1: "Fear", 2: "Anger", 3: "Happiness", 4: "Neutral", 5: "Sad", 6: "Suprise"}

# Change the video file path here
video_file = '2024-03-19 13-45-28.mkv'
cap = cv2.VideoCapture(video_file)

parent_folder = "parent"
os.makedirs(parent_folder, exist_ok=True)
for emotion in emotion_dict.values():
    os.makedirs(os.path.join(parent_folder, emotion), exist_ok=True)

print("[INFO] loading face detection model...")
prototxt_path = "deploy.prototxt.txt"
model_path = "res10_300x300_ssd_iter_140000.caffemodel"
net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

print("[INFO] starting video stream...")

# Number of frames to skip
skip_frames = 10
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1
    if frame_count % skip_frames != 0:
        continue

    frame = cv2.resize(frame, (1280, 720))
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            face_color = frame[startY:endY, startX:endX]
            if face_color.size == 0:
                print("Face color ROI is empty. Skipping...")
                continue

            resized_face_color = cv2.resize(face_color, (224, 224))
            model_input_img = np.expand_dims(resized_face_color, axis=0)
            model_input_img = cv2.cvtColor(model_input_img[0], cv2.COLOR_BGR2RGB)
            model_input_img = np.expand_dims(model_input_img, axis=0)

            emotion_prediction = emotion_model.predict(model_input_img)
            maxindex = int(np.argmax(emotion_prediction))
            detected_emotion = emotion_dict[maxindex]

            face_filename = f"{parent_folder}/{detected_emotion}/face_{len(os.listdir(os.path.join(parent_folder, detected_emotion)))}.jpg"
            cv2.imwrite(face_filename, face_color)

            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            cv2.putText(frame, detected_emotion, (startX + 5, startY - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Emotion Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
