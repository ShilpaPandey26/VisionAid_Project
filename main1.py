# # from voice_interaction import listen_for_command, speak
# # from document_search import search_document
# # from summarizer import summarize_document, extract_pdf_content, extract_docx_content
# # import os
# # from voice_interaction import listen_for_command, speak

# # def main():
# #     speak("Welcome! What document would you like me to summarize?")
    
# #     # Listen to the user's command (the document name)
# #     doc_name = listen_for_command()

# #     if doc_name:
# #         # Search for the document
# #         file_path = search_document(doc_name, search_path=os.path.expanduser("~"))
        
# #         if file_path:
# #             speak(f"Document found: {file_path}")
            
# #             # Extract and summarize content based on the file type
# #             if file_path.endswith(".pdf"):
# #                 content = extract_pdf_content(file_path)
# #             elif file_path.endswith(".docx"):
# #                 content = extract_docx_content(file_path)
# #             else:
# #                 with open(file_path, 'r') as file:
# #                     content = file.read()
            
# #             # Summarize the content
# #             summary = summarize_document(file_path)
            
# #             # Speak the summary aloud
# #             speak("Here is the summary:")
# #             speak(summary)
# #         else:
# #             speak("Sorry, I couldn't find the document.")
# #     else:
# #         speak("I couldn't hear a document name clearly.")

# # if __name__ == "__main__":
# #     main()
# import tkinter as tk
# from tkinter import scrolledtext
# from voice_interaction import listen_for_command, speak
# from document_search import search_document
# from summarizer import summarize_document, extract_pdf_content, extract_docx_content
# import os

# class VoiceSummarizerApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Voice Document Summarizer")
#         self.root.geometry("500x400")

#         # Welcome label
#         self.label = tk.Label(root, text="Welcome to the Voice Document Summarizer!", font=("Arial", 14))
#         self.label.pack(pady=10)

#         # Text area to display the document path and summary
#         self.text_area = scrolledtext.ScrolledText(root, width=60, height=15, font=("Arial", 12))
#         self.text_area.pack(pady=10)

#         # Status bar
#         self.status = tk.StringVar()
#         self.status_label = tk.Label(root, textvariable=self.status, font=("Arial", 10), fg="grey")
#         self.status_label.pack(pady=10)

#         # Start listening for the document name
#         self.start_listening()

#     def start_listening(self):
#         welcome_message = "Welcome to the Voice Document Summarizer. Please say the name of the document you want to summarize."
#         self.status.set(welcome_message)
#         speak(welcome_message)
#         self.listen_for_document_name()

#     def listen_for_document_name(self):
#         self.status.set("Listening for the document name...")
#         self.root.update()  # Update the GUI

#         # Listen for command
#         doc_name = listen_for_command()

#         if doc_name.lower() == "exit":
#             self.status.set("Exiting application.")
#             speak("Exiting application.")
#             self.root.destroy()
#             exit()
#             return

        
#         if doc_name:
#             self.status.set(f"You said: {doc_name}. Processing the document...")
#             speak(f"You said: {doc_name}. Processing the document...")
#             self.process_document(doc_name)
#         else:
#             error_message = "I couldn't hear a document name clearly."
#             self.status.set(error_message)
#             speak(error_message)
#             self.listen_for_document_name()  # Retry listening

#     def process_document(self, doc_name):
#         file_path = search_document(doc_name, search_path=os.path.expanduser("~"))

#         if file_path:
#             self.status.set(f"Document found: {file_path}")
#             self.text_area.insert(tk.END, f"Document found: {file_path}\n")
#             # speak(f"Document found: {file_path}")
#             speak("Document found. Processing the content.")

#             # Extract and summarize content based on the file type
#             if file_path.endswith(".pdf"):
#                 content = extract_pdf_content(file_path)
#             elif file_path.endswith(".docx"):
#                 content = extract_docx_content(file_path)
#             else:
#                 with open(file_path, 'r') as file:
#                     content = file.read()

#             self.status.set("Summarizing...")
#             speak("Summarizing the document...")
#             summary = summarize_document(file_path)

#             # Display the summary
#             self.text_area.insert(tk.END, "Here is the summary:\n")
#             self.text_area.insert(tk.END, summary)
#             speak("Here is the summary:")
#             speak(summary)

#             # Restart the process to listen for another document name
#             self.listen_for_document_name()
#         else:
#             error_message = "Sorry, I couldn't find the document."
#             self.status.set(error_message)
#             speak(error_message)
#             self.listen_for_document_name()  # Retry listening



# if __name__ == "__main__":
#     root = tk.Tk()
#     app = VoiceSummarizerApp(root)
#     root.mainloop()












# new




import sys
import tkinter as tk
from tkinter import scrolledtext
from voice_interaction import listen_for_command, speak
from document_search import search_document
from summarizer import summarize_document, extract_pdf_content, extract_docx_content
import os

class VoiceSummarizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Document Summarizer")
        self.root.geometry("500x400")

        # Welcome label
        self.label = tk.Label(root, text="Welcome to the Voice Document Summarizer!", font=("Arial", 14))
        self.label.pack(pady=10)

        # Text area to display the document path and summary
        self.text_area = scrolledtext.ScrolledText(root, width=60, height=15, font=("Arial", 12))
        self.text_area.pack(pady=10)

        # Status bar
        self.status = tk.StringVar()
        self.status_label = tk.Label(root, textvariable=self.status, font=("Arial", 10), fg="grey")
        self.status_label.pack(pady=10)

        # Start listening for the document name
        self.start_listening()

    def start_listening(self):
        welcome_message = "Welcome to the Voice Document Summarizer. Please say the name of the document you want to summarize."
        self.status.set(welcome_message)
        speak(welcome_message)
        self.listen_for_document_name()

    # def listen_for_document_name(self):
    #     self.status.set("Listening for the document name...")
    #     self.root.update()  # Update the GUI

    #     # Listen for command
    #     doc_name = listen_for_command()

    #     if doc_name.lower() == "exit":
    #         self.status.set("Exiting application.")
    #         speak("Exiting application.")
    #         self.root.destroy()  # Close the Tkinter window
    #         sys.exit()  # Completely stop the script
    #         return

    #     if doc_name:
    #         self.status.set(f"You said: {doc_name}. Processing the document...")
    #         speak(f"You said: {doc_name}. Processing the document...")
    #         self.process_document(doc_name)
    #     else:
    #         error_message = "I couldn't hear a document name clearly."
    #         self.status.set(error_message)
    #         speak(error_message)
    #         self.listen_for_document_name()  # Retry listening

    def listen_for_document_name(self):
        self.status.set("Listening for the document name...")
        self.root.update()  # Update the GUI

        # Listen for command
        doc_name = listen_for_command()

        # Check if doc_name is None before using .lower()
        if doc_name is None:
            error_message = "I couldn't hear a document name clearly."
            self.status.set(error_message)
            speak(error_message)
            self.listen_for_document_name()  # Retry listening
            return

        if doc_name.lower() == "exit":
            self.status.set("Exiting application.")
            speak("Exiting application.")
            self.root.destroy()  # Close the GUI window
            return

        self.status.set(f"You said: {doc_name}. Processing the document...")
        speak(f"You said: {doc_name}. Processing the document...")
        self.process_document(doc_name)

    
    
    
    def process_document(self, doc_name):
        file_path = search_document(doc_name, search_path=os.path.expanduser("~"))

        if file_path:
            self.status.set(f"Document found: {file_path}")
            self.text_area.insert(tk.END, f"Document found: {file_path}\n")
            speak("Document found. Processing the content.")

            # Extract and summarize content based on the file type
            if file_path.endswith(".pdf"):
                content = extract_pdf_content(file_path)
            elif file_path.endswith(".docx"):
                content = extract_docx_content(file_path)
            else:
                with open(file_path, 'r') as file:
                    content = file.read()

            self.status.set("Summarizing...")
            speak("Summarizing the document...")
            summary = summarize_document(file_path)

            # Display the summary
            self.text_area.insert(tk.END, "Here is the summary:\n")
            self.text_area.insert(tk.END, summary)
            speak("Here is the summary:")
            speak(summary)

            # Restart the process to listen for another document name
            self.listen_for_document_name()
        else:
            error_message = "Sorry, I couldn't find the document."
            self.status.set(error_message)
            speak(error_message)
            self.listen_for_document_name()  # Retry listening

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceSummarizerApp(root)
    root.mainloop()
