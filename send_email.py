import os
import sounddevice as sd
import numpy as np
import wavio
import speech_recognition as sr
import pyttsx3
import smtplib
import imaplib
import email


# Initialize text-to-speech engine
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Function to record audio using sounddevice
def record_audio(file_name="recording.wav", duration=10, samplerate=44100):
    speak("Listening...")
    print("Recording...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is finished
    wavio.write(file_name, audio_data, samplerate, sampwidth=2)
    print("Recording complete.")
    return file_name


# Function to listen to user's voice and convert it to text
def listen_to_user(is_email=False):
    file_name = record_audio()
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(file_name) as source:
            audio = recognizer.record(source)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")

            if is_email:
                # Normalize text for email processing
                command = (
                    command.replace(" at the rate ", "@")
                           .replace(" dot ", ".")
                           .replace(" ", "")
                )
            return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand. Please try again.")
        return None
    except sr.RequestError:
        speak("Network error. Please check your internet connection.")
        return None


# Map text-based numbers to integers
def text_to_number(text):
    mapping = {
        "one": 1,
        "two": 2,
        "three": 3
    }
    return mapping.get(text, None)


# Function to send an email
def send_email():
    speak("Please say your email address.")
    sender_email = listen_to_user(is_email=True)

    if not sender_email:
        return

    sender_password = os.getenv("EMAIL_APP_PASSWORD")  # Fetch from environment variables
    if not sender_password:
        speak("App password is not set. Please check your configuration.")
        return

    speak("Say the recipient's email address.")
    recipient_email = listen_to_user(is_email=True)

    if not recipient_email:
        return

    speak("What is the subject of the email?")
    subject = listen_to_user()

    if not subject:
        return

    speak("What should I write in the email body?")
    body = listen_to_user()

    if not body:
        return

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(sender_email, recipient_email, message)
            speak("Email sent successfully!")
    except Exception as e:
        speak("Failed to send email. Please check the details and try again.")
        print(f"Error: {e}")


# Function to read emails
def read_emails():
    speak("Please say your email address.")
    email_user = listen_to_user(is_email=True)

    if not email_user:
        return

    email_password = os.getenv("EMAIL_APP_PASSWORD")  # Fetch from environment variables
    if not email_password:
        speak("App password is not set. Please check your configuration.")
        return

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, email_password)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()
        if not email_ids:
            speak("Your inbox is empty.")
            return

        latest_email_id = email_ids[-1]
        status, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]

        msg = email.message_from_bytes(raw_email)
        speak("Here is your latest email:")
        print("From:", msg["From"])
        speak(f"From: {msg['From']}")
        print("Subject:", msg["Subject"])
        speak(f"Subject: {msg['Subject']}")

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    speak(part.get_payload(decode=True).decode())
        else:
            speak(msg.get_payload(decode=True).decode())

        mail.logout()
    except Exception as e:
        speak("Failed to read emails. Please check the details and try again.")
        print(f"Error: {e}")


# Main function to handle user commands
def virtual_assistant():
    speak("Welcome to your virtual assistant.")
    while True:
        speak("Options: 1 for sending an email, 2 for reading emails, or 3 to exit.")
        print("Options: 1. Send an email  2. Read emails  3. Exit")

        command = listen_to_user()

        if not command:
            continue

        # Convert voice input to number
        choice = text_to_number(command)

        if choice == 1:
            send_email()
        elif choice == 2:
            read_emails()
        elif choice == 3:
            speak("Goodbye!")
            break
        else:
            speak("Invalid choice. Please say one, two, or three.")


# Run the virtual assistant
if __name__ == "__main__":
    if not os.getenv("EMAIL_APP_PASSWORD"):
        print("Warning: EMAIL_APP_PASSWORD environment variable is not set. Please configure it.")
    virtual_assistant()