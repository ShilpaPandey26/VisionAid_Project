# ui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from voice_interaction import speak, listen  # Import your TTS and speech recognition functions
from document_search import search_documents  # Import document search function
from summarizer import summarize_document  # Import summarizer function

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Text Files", "*.txt")])
    if file_path:
        # Call your document summarizer function
        try:
            summary = summarize_document(file_path)
            messagebox.showinfo("Summary", summary)
        except Exception as e:
            messagebox.showerror("Error", str(e))

def listen_and_summarize():
    speak("Please say the name of the document you want to summarize.")
    document_name = listen()  # This will listen for the document name
    if document_name:
        file_path = search_documents(document_name)  # Implement this function to search for documents
        if file_path:
            summary = summarize_document(file_path)
            speak(summary)  # Speak out the summary
        else:
            speak("Document not found. Please try again.")

def create_ui():
    root = tk.Tk()
    root.title("Voice Summarizer")
    root.geometry("400x300")

    label = tk.Label(root, text="Welcome to Voice Summarizer", font=("Helvetica", 16))
    label.pack(pady=20)

    select_button = tk.Button(root, text="Select Document", command=select_file)
    select_button.pack(pady=10)

    listen_button = tk.Button(root, text="Listen and Summarize", command=listen_and_summarize)
    listen_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_ui()
