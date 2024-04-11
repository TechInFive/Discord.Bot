import threading
import tkinter as tk
from tkinter import scrolledtext

from AudioService import AudioService
from OpenAIService import OpenAIService

class InteractiveDashboard:
    def __init__(self, title="Interactive Dashboard", size="800x600"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(size)

        # Creating a frame for text area and buttons
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.audio_service = AudioService()  # Assume AudioService is properly imported
        self.open_ai_service = OpenAIService()

        # Adding attributes for recording state and button reference
        self.is_recording = False
        self.record_button = None
        self.initialize_ui()

    def add_button(self, label, command):
        """Adds a button to the dashboard."""
        button = tk.Button(self.buttons_frame, text=label, command=command)
        button.pack(side=tk.LEFT, padx=10, pady=5)
        return button

    def display_text(self, text):
        """Displays the given text in the text area, clearing the previous content."""
        self.text_area.configure(state='normal')
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, text)
        self.text_area.configure(state='disabled')
    
    def append_text(self, text):
        """Appends the given text to the existing content in the text area."""
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.configure(state='disabled')

    def initialize_ui(self):
        """Sets up the UI elements including the record button."""
        # Creating a scrolled text area for output
        self.text_area = scrolledtext.ScrolledText(
            self.frame, wrap=tk.WORD, state='disabled', exportselection=True)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(fill=tk.X, expand=False)

        # Adds a record button that toggles between 'Start' and 'Stop'.
        self.record_button = self.add_button(label="Start", command=self.toggle_recording)

    def toggle_recording(self):
        """Toggles the recording state and updates button text."""
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        """Starts the recording."""
        self.is_recording = True
        self.record_button.config(text="Stop")
        self.append_text("Recording started...")
        self.audio_service.start_recording("output.wav")  # Specify the desired WAV file path

    def stop_recording(self):
        """Stops the recording."""
        self.is_recording = False
        self.record_button.config(text="Start")
        self.audio_service.stop_recording()
        self.append_text("Recording stopped.")

        threading.Thread(target=self.process_audio, daemon=True).start()

    def process_audio(self):
        self.audio_service.convert_wav_2_mp3("output.wav", "output.mp3")
        transcription = self.open_ai_service.create_transcription("output.mp3")
        chat_message = transcription.text
        # Use self.root.after to interact with the UI from the background thread
        self.root.after(0, self.append_text, chat_message)

        messages = [
            { "role": "system", "content": "Please be concise." },
            { "role": "user", "content": chat_message }
        ]
        completion = self.open_ai_service.simple_completion(messages)
        chat_response = completion.choices[0].message.content
        # Schedule append_text to run on the main thread
        self.root.after(0, self.append_text, chat_response)

        self.open_ai_service.create_speech_file("echo", chat_response, "response.mp3")
        self.audio_service.play("response.mp3")

    def run(self):
        """Starts the main loop of the dashboard."""
        self.root.mainloop()

# Example of using the InteractiveDashboard
if __name__ == "__main__":
    dashboard = InteractiveDashboard()
    dashboard.display_text("Welcome to the Interactive Dashboard\n")
    dashboard.run()






