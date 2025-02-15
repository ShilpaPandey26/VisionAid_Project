import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()

def listen_for_command():
    fs = 44100  # Sample rate
    seconds = 5  # Duration of recording

    print("Recording... Speak now.")
    
    # Record audio from the microphone
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    audio = np.squeeze(audio)

    # Convert numpy array to audio data that speech_recognition can process
    audio_data = sr.AudioData(audio.tobytes(), fs, 2)
    
    try:
        command = recognizer.recognize_google(audio_data)
        print(f"User said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        speak("Could not request results; check your internet connection.")
        return None

# def speak(text):
#     engine = pyttsx3.init()
#     engine.say(text)
#     engine.runAndWait()

#new

def speak(text):
    engine = pyttsx3.init()
    
    # Set speaking rate (reduce to slow down)
    engine.setProperty('rate', 150)  # Default is usually around 200-250, reduce it

    # Set voice to an Indian English accent
    voices = engine.getProperty('voices')
    for voice in voices:
        if "Indian" in voice.name or "en-in" in voice.id:  # Match Indian English voices
            engine.setProperty('voice', voice.id)
            break

    engine.say(text)
    engine.runAndWait()

