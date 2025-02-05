import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
import pygame
import sounddevice as sd
import numpy as np
import threading
import time
from pydub.playback import play

# Initialize Pygame for audio playback
pygame.mixer.init()

class SimpleDAW(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Full-Featured DAW")
        self.geometry("1600x900")
        self.config(bg="#2f2f2f")
        
        # Initialize components
        self.create_widgets()
        self.tracks = []  # List to store loaded tracks
        self.effects = []  # List to store applied effects
        self.is_playing = False

    def create_widgets(self):
        """Create the DAW's main components and layout."""
        
        # Control Buttons: Play, Stop, Record
        self.control_frame = tk.Frame(self, bg="#2f2f2f")
        self.control_frame.pack(pady=10)
        
        self.play_button = self.create_button(self.control_frame, "Play", self.play_tracks)
        self.play_button.grid(row=0, column=0, padx=10)
        
        self.stop_button = self.create_button(self.control_frame, "Stop", self.stop_tracks)
        self.stop_button.grid(row=0, column=1, padx=10)
        
        self.record_button = self.create_button(self.control_frame, "Record", self.record_audio)
        self.record_button.grid(row=0, column=2, padx=10)
        
        self.load_button = self.create_button(self.control_frame, "Load Track", self.load_track)
        self.load_button.grid(row=0, column=3, padx=10)

        self.export_button = self.create_button(self.control_frame, "Export", self.export_audio)
        self.export_button.grid(row=0, column=4, padx=10)

        # Track List and Effects Panel
        self.track_effects_frame = tk.Frame(self, bg="#2f2f2f")
        self.track_effects_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Track Listbox
        self.track_listbox = self.create_listbox(self.track_effects_frame)
        self.track_listbox.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Effects Listbox
        self.effects_listbox = self.create_listbox(self.track_effects_frame)
        self.effects_listbox.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        # Timeline (basic, no interaction yet)
        self.timeline_frame = tk.Frame(self, bg="#2f2f2f")
        self.timeline_frame.pack(pady=20, fill=tk.X)

        self.canvas = tk.Canvas(self.timeline_frame, bg="#1f1f1f", height=100)
        self.canvas.pack(fill=tk.X)
        
        self.timeline_cursor = self.canvas.create_line(0, 0, 0, 100, fill="red", width=2)

    def create_button(self, parent, text, command):
        """Helper function to create styled buttons."""
        button = tk.Button(parent, text=text, command=command, bg="#444444", fg="#FFFFFF", font=("Helvetica", 12), relief="flat")
        button.config(height=2, width=12)
        return button

    def create_listbox(self, parent):
        """Helper function to create styled listboxes."""
        listbox = tk.Listbox(parent, bg="#1f1f1f", fg="#FFFFFF", font=("Helvetica", 10), relief="flat", selectmode=tk.SINGLE)
        return listbox

    def load_track(self):
        """Load an audio track into the DAW."""
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.ogg")])
        if file_path:
            track = pygame.mixer.Sound(file_path)
            self.tracks.append(track)
            self.track_listbox.insert(tk.END, file_path.split("/")[-1])
            self.update_timeline()

    def play_tracks(self):
        """Play all loaded tracks."""
        if not self.is_playing:
            self.is_playing = True
            self.update_timeline_cursor()

            for track in self.tracks:
                threading.Thread(target=self.play_track).start()

    def play_track(self):
        """Simulate track playback."""
        for track in self.tracks:
            track.play()
            time.sleep(3)  # Placeholder for track length

    def stop_tracks(self):
        """Stop all playing tracks."""
        pygame.mixer.stop()
        self.is_playing = False

    def record_audio(self):
        """Record audio from the default input device."""
        self.recording = True
        fs = 44100  # Sample rate
        duration = 5  # Duration in seconds
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
        sd.wait()  # Wait for the recording to finish
        self.recording = False
        audio_segment = AudioSegment(recording.tobytes(), frame_rate=fs, sample_width=2, channels=2)
        self.tracks.append(audio_segment)
        self.track_listbox.insert(tk.END, "New Recorded Track")

    def export_audio(self):
        """Export all tracks as a single WAV file."""
        try:
            combined = AudioSegment.silent(duration=0)
            for track in self.tracks:
                if isinstance(track, pygame.mixer.Sound):
                    samples = np.array(track.get_raw())
                    audio = AudioSegment(samples.tobytes(), frame_rate=44100, sample_width=2, channels=2)
                    combined = combined.append(audio)
                elif isinstance(track, AudioSegment):
                    combined = combined.append(track)
            
            export_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
            if export_path:
                combined.export(export_path, format="wav")
                messagebox.showinfo("Export", "Audio exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting: {e}")

    def update_timeline(self):
        """Update the timeline to reflect track positions."""
        self.canvas.delete("all")  # Clear previous content
        for i, track in enumerate(self.tracks):
            # Example: Each track starts at a new position
            self.canvas.create_line(i * 100, 0, i * 100, 100, fill="blue", width=5)

    def update_timeline_cursor(self):
        """Update the position of the timeline cursor."""
        if self.is_playing:
            self.canvas.coords(self.timeline_cursor, 0, 0, 0, 100)  # Placeholder to move cursor

if __name__ == "__main__":
    app = SimpleDAW()
    app.mainloop()
