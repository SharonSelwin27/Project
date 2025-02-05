import numpy as np
import scipy.io.wavfile as wav
import customtkinter as ctk
from tkinter import filedialog

# Global variable to store the status label reference
status_label = None

# Spectratyping function to convert text data to audio waveform
def spectratype_to_audio(data):
    # Convert each character to its ASCII value
    ascii_values = np.array([ord(char) for char in data])
    
    # Normalize the data to generate waveform
    audio_data = np.interp(ascii_values, (0, 255), (-1, 1))
    
    # Rescale to 16-bit PCM
    audio_data = np.int16(audio_data * 32767)
    
    return audio_data

# Function to load text file, convert it to audio, and save as .wav
def convert_to_wav():
    file_path = filedialog.askopenfilename(title="Open Text File", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            data = file.read()
        
        # Convert the data to audio using spectratyping
        audio_data = spectratype_to_audio(data)
        
        # Define the sample rate (44100 Hz is CD-quality)
        sample_rate = 44100
        
        # Save the audio as a .wav file
        wav_output_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
        if wav_output_path:
            wav.write(wav_output_path, sample_rate, audio_data)
            # Update the status label to show the saved file path
            status_label.configure(text=f"File saved as: {wav_output_path}")

# Setting up the GUI
def setup_gui():
    global status_label  # Access the global status_label variable
    app = ctk.CTk()
    app.title("Spectratyping to WAV Converter")
    app.geometry("400x300")

    convert_button = ctk.CTkButton(app, text="Convert Text to WAV", command=convert_to_wav)
    convert_button.pack(pady=20)

    # Initialize status_label here
    status_label = ctk.CTkLabel(app, text="Select a text file to convert to WAV", width=300)
    status_label.pack(pady=20)
    
    app.mainloop()

if __name__ == "__main__":
    setup_gui()
