import speech_recognition as sr
from textblob import TextBlob

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something about your day...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Speech not recognized"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

def detect_mood(text):
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity

    if sentiment > 0:
        return "happy"
    elif sentiment < 0:
        return "sad"
    else:
        return "neutral"

# Get user's speech about their day
user_input = speech_to_text()
print(f"You said: {user_input}")

# Detect the mood of the author's day
mood = detect_mood(user_input)
print(f"Author's mood of the day: {mood}")
