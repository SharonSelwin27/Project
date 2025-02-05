import numpy as np
import scipy.io.wavfile as wav
import customtkinter as ctk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import LogNorm

# Function to update the spectrogram plot
def update_spectrogram(audio_data, sample_rate, time_window):
    # Perform a short-time Fourier transform (STFT)
    _, _, Sxx, _ = plt.specgram(audio_data, NFFT=1024, Fs=sample_rate, noverlap=512, scale='dB', mode='default')
    
    # Normalize the spectrogram
    ax.clear()
    ax.imshow(Sxx, aspect='auto', origin='lower', cmap='inferno', norm=LogNorm(vmin=1e-2, vmax=1e2))
    ax.set_xlabel('Time')
    ax.set_ylabel('Frequency (Hz)')
    ax.set_title('Spectrogram')
    ax.set_ylim(0, sample_rate // 2)  # Limit the frequency to Nyquist
    canvas.draw()

# Function to load the audio file, analyze and display the spectrogram
def load_and_analyze_audio():
    file_path = filedialog.askopenfilename(title="Open WAV File", filetypes=[("WAV Files", "*.wav")])
    if file_path:
        # Read the WAV file
        sample_rate, audio_data = wav.read(file_path)

        # If the audio data has multiple channels (stereo), convert to mono by averaging the channels
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)
        
        # Update the spectrogram with the loaded audio data
        update_spectrogram(audio_data, sample_rate, time_window=1024)

# Setting up the GUI
def setup_gui():
    global ax, canvas  # Global variables for the plot and canvas

    # Create main app window
    app = ctk.CTk()
    app.title("Spectrascope")
    app.geometry("800x600")

    # Button to load and analyze the WAV file
    analyze_button = ctk.CTkButton(app, text="Load and Analyze Audio", command=load_and_analyze_audio)
    analyze_button.pack(pady=20)

    # Create a frame to hold the spectrogram plot
    plot_frame = ctk.CTkFrame(app)
    plot_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Create the plot for the spectrogram
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlabel("Time")
    ax.set_ylabel("Frequency (Hz)")

    # Embed the plot in the Tkinter window using matplotlib's FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    app.mainloop()

if __name__ == "__main__":
    setup_gui()
