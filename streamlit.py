import streamlit as st
from textblob import TextBlob
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
import requests

# Set your Google Cloud credentials environment variable (replace 'YOUR_CREDENTIALS' with your actual path)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "YOUR_CREDENTIALS.json"

# Initialize variables to store mood data
mood_data = {'Happy': 0, 'Sad': 0, 'Neutral': 0}
weekly_mood = []

# Function to update mood data and weekly mood
def update_mood(text):
    global mood_data
    global weekly_mood

    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity

    if sentiment > 0:
        mood = 'Happy'
    elif sentiment < 0:
        mood = 'Sad'
    else:
        mood = 'Neutral'

    mood_data[mood] += 1
    weekly_mood.append(mood)

# Function to analyze weekly overall mood
def get_weekly_mood():
    week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    week_mood = [mood_data[m] for m in weekly_mood if (datetime.now() - timedelta(days=datetime.now().weekday())) <= week_start]
    weekly_mood.clear()

    if not week_mood:
        return "No data"
    
    avg_mood = sum(week_mood) / len(week_mood)
    
    if avg_mood > 0:
        return 'Happy'
    elif avg_mood < 0:
        return 'Sad'
    else:
        return 'Neutral'

# Streamlit app
st.title("Mood Analyzer")

# Record and analyze speech
if st.button("Record and Analyze"):
    user_input = recognize_speech()
    update_mood(user_input)
    st.write(f"You said: {user_input}")
    st.write(f"Mood: {get_weekly_mood()}")

# Display mood statistics as a pie chart
st.write("Mood Statistics:")
fig, ax = plt.subplots()
ax.pie(mood_data.values(), labels=mood_data.keys(), autopct='%1.1f%%', startangle=140)
ax.axis('equal')
st.pyplot(fig)

# Display weekly overall mood
st.write(f"Weekly Overall Mood: {get_weekly_mood()}")

def recognize_speech():
    audio_data = st.audio("Recording...", format="audio/wav")
    
    if audio_data:
        # Convert audio data to text using Google Cloud Speech-to-Text API
        response = transcribe_audio(audio_data)
        return response
    else:
        return "Speech not recognized"

def transcribe_audio(audio_data):
    endpoint = "https://speech.googleapis.com/v1/speech:recognize"
    data = {
        "config": {"encoding": "LINEAR16", "sampleRateHertz": 16000, "languageCode": "en-US"},
        "audio": {"content": audio_data},
    }

    response = requests.post(
        endpoint, json=data
    )

    if response.status_code == 200:
        result = response.json()
        if "results" in result:
            transcripts = [alt["transcript"] for alt in result["results"][0]["alternatives"]]
            return "\n".join(transcripts)
    
    return "Speech not recognized"
