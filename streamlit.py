import streamlit as st
import cv2
import numpy as np
from tensorflow import keras
from PIL import Image

# Load your trained model for face detection (you might need a separate model or a pre-trained model for this)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load your trained model for emotion recognition
model = keras.models.load_model("your_emotion_model.h5")

st.title("Real-time Face Emotion Detection")

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Preprocess the detected face
        face = gray[y:y + h, x:x + w]
        face = cv2.resize(face, (48, 48))
        face = np.expand_dims(face, axis=0)
        face = face / 255.0

        # Use your trained model to predict the emotion
        emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]
        emotion_probabilities = model.predict(face)
        emotion_index = np.argmax(emotion_probabilities)
        emotion_label = emotion_labels[emotion_index]

        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the emotion label
        cv2.putText(frame, emotion_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Convert the OpenCV frame to a format Streamlit can display
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the frame with the emotion labels
    st.image(frame, use_column_width=True)
    st.write("Emotion: " + emotion_label)

# Close the webcam
cap.release()
