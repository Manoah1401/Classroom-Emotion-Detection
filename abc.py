import cv2
import numpy as np
import os
from keras.models import model_from_json
from mtcnn.mtcnn import MTCNN

emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
# Load json and create model
json_file = open('emotion_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)

# Load weights into the model
emotion_model.load_weights("emotion_model.h5")
print("Loaded model from disk")

# Start the webcam feed
cap = cv2.VideoCapture(0)

# Initialize MTCNN face detector
detector = MTCNN()

# Create directories for each emotion class if they do not exist
for emotion in emotion_dict.values():
    os.makedirs(emotion, exist_ok=True)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (1280, 720))
    
    # Use MTCNN to detect faces
    face_detections = detector.detect_faces(frame)

    # Process each detected face
    for face in face_detections:
        (x, y, w, h) = face['box']
        roi_gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)[y:y+h, x:x+w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

        # Predict the emotions
        emotion_prediction = emotion_model.predict(cropped_img)
        maxindex = int(np.argmax(emotion_prediction))
        detected_emotion = emotion_dict[maxindex]
        
        # Save the image frame with the corresponding class label
        img_filename = f"{detected_emotion}/frame_{len(os.listdir(detected_emotion))}.jpg"
        cv2.imwrite(img_filename, frame[y:y+h, x:x+w])  # Save only the face region
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, detected_emotion, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow('Emotion Detection', frame)
    
    # Check for user input to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
