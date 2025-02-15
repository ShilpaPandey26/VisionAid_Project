import tkinter as tk
import subprocess
import pyttsx3
import speech_recognition as sr
import threading

# Initialize Tkinter window
root = tk.Tk()
root.title("AI Accessibility Hub")
root.geometry("1024x768")
root.configure(bg="#1E1E1E")  # Dark theme for better accessibility
root.state('zoomed')  # Start maximized

# Styling configuration
BUTTON_STYLE = {
    "font": ("Arial", 16, "bold"),
    "fg": "white",
    "bg": "#007BFF",
    "activebackground": "#0056b3",
    "bd": 4,
    "relief": "raised",
    "width": 40,
    "height": 2
}

LABEL_STYLE = {
    "font": ("Arial", 18, "bold"),
    "fg": "white",
    "bg": "#1E1E1E"
}

EXIT_BUTTON_STYLE = {
    **BUTTON_STYLE,
    "bg": "#DC3545",
    "activebackground": "#A71C2C"
}

def speak(text):
    """Function to convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    """Function to recognize voice input."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        listening_label.config(text="Listening...", fg="yellow")
        root.update()
        
        speak("Please say Send Email, Summarize Documentation, Navigation, or Exit to choose an option.")
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            listening_label.config(text="", fg="white")
            root.update()
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            listening_label.config(text="", fg="white")
            speak("Sorry, I could not understand. Please try again.")
            return None
        except sr.RequestError:
            listening_label.config(text="", fg="white")
            speak("There was an error with the speech recognition service.")
            return None

def run_script(script_name):
    """Function to execute a Python script."""
    try:
        process = subprocess.Popen(["python", script_name])
        speak(f"Running {script_name}")
        print(f"Running: {script_name}")
        status_label.config(text=f"Running: {script_name}", fg="green")
        process.wait()
        status_label.config(text="Idle", fg="white")
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        speak("Error running the script")
        status_label.config(text="Error Running Script", fg="red")

def voice_selection():
    """Function to continuously take voice input and run the corresponding script."""
    while True:
        command = listen()
        if command:
            if "send email" in command:
                run_script("send_email.py")
            elif "documentation" in command:
                run_script("main1.py")
            elif "navigation" in command:
                run_script("app.py")
            elif "exit" in command:
                speak("Exiting AI Accessibility Dashboard.")
                root.quit()
                break
            else:
                speak("Invalid choice. Please try again.")

def start_voice_thread():
    threading.Thread(target=voice_selection, daemon=True).start()

# Title Label
title_label = tk.Label(root, text="AI Accessibility Dashbord", **LABEL_STYLE)
title_label.pack(pady=20)

# Listening Status Label
listening_label = tk.Label(root, text="", **LABEL_STYLE)
listening_label.pack()

# Status Label
status_label = tk.Label(root, text="Idle", **LABEL_STYLE)
status_label.pack(pady=10)

# Button Frame
button_frame = tk.Frame(root, bg="#1E1E1E")
button_frame.pack(pady=20)

def create_button(text, script):
    return tk.Button(button_frame, text=text, command=lambda: run_script(script), **BUTTON_STYLE)

# Buttons for functionalities
btn1 = create_button("\U0001F4E7 Send Email", "send_email.py")
btn1.pack(pady=10)

btn2 = create_button("\U0001F4C4 Summarize Documentation", "main1.py")
btn2.pack(pady=10)

btn3 = create_button("\U0001F9ED Navigation", "app.py")

btn3.pack(pady=10)

# Exit Button
btn_exit = tk.Button(root, text="\u274C Exit", command=root.quit, **EXIT_BUTTON_STYLE)
btn_exit.pack(pady=20)

# Start voice thread
speak("Welcome to AI Accessibility Dashboard.")
root.after(1000, start_voice_thread)

# Run the GUI
root.mainloop()
