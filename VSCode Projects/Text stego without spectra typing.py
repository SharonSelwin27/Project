import customtkinter as ctk
from tkinter import filedialog, messagebox
import numpy as np
import wave
from scipy.fft import fft, ifft

# ----------------- Application Configuration -----------------
ctk.set_appearance_mode("dark")  # Set dark mode
root = ctk.CTk()
root.title("GRAPHY")
root.geometry("1024x768")
root.configure(bg="#1e1e1e")

# Global variables
main_content = ctk.CTkFrame(root)  # Main content area
main_content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

entry_message = None
entry_shift = None

# ----------------- Helper Functions -----------------
def clear_main_content():
    """Clears all widgets from the main content frame."""
    for widget in main_content.winfo_children():
        widget.destroy()

def get_shift_value():
    """Gets a valid integer shift value for Caesar Cipher."""
    shift_str = entry_shift.get()
    if not shift_str.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid integer for the Caesar Cipher shift.")
        return None
    return int(shift_str)

# ----------------- Caesar Cipher Encryption & Decryption -----------------
def caesar_cipher_encrypt(plaintext, shift):
    """Encrypts a message using Caesar Cipher."""
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            encrypted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
            ciphertext += encrypted_char
        else:
            ciphertext += char
    return ciphertext

def caesar_cipher_decrypt(ciphertext, shift):
    """Decrypts a message using Caesar Cipher."""
    return caesar_cipher_encrypt(ciphertext, -shift)

# ----------------- Spectratyping Functions -----------------
def text_to_frequency_data(text):
    """Converts the text (ciphered message) into frequency data."""
    ascii_values = [ord(char) for char in text]
    sample_rate = 44100  # Standard audio sample rate
    duration = 0.5  # Duration for each note (in seconds)
    signal = np.array([])

    for value in ascii_values:
        freq = 440 + (value % 100)  # Base frequency + offset from the ASCII value
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        sine_wave = np.sin(2 * np.pi * freq * t)
        signal = np.concatenate((signal, sine_wave))

    return signal, sample_rate

def encode_message_with_spectratyping(cipher_message):
    """Encodes the ciphered message using spectratyping."""
    signal, sample_rate = text_to_frequency_data(cipher_message)

    file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
    if file_path:
        with wave.open(file_path, 'w') as file:
            file.setnchannels(1)  # Mono sound
            file.setsampwidth(2)  # 2 bytes per sample (16-bit)
            file.setframerate(sample_rate)

            samples = np.int16(signal * 32767)  # Scaling to 16-bit range
            file.writeframes(samples.tobytes())
        messagebox.showinfo("Encoding Complete", f"Message saved as {file_path}")

def decode_message_from_spectratyping(file_path):
    """Decodes the encoded message from a .wav file."""
    with wave.open(file_path, 'r') as file:
        sample_rate = file.getframerate()
        frames = file.readframes(file.getnframes())
        signal = np.frombuffer(frames, dtype=np.int16)

    transformed_signal = fft(signal)
    decoded_message = []

    for freq in transformed_signal[:len(signal) // 2]:
        magnitude = np.abs(freq)
        if magnitude > 1000:  # Threshold to filter out noise
            ascii_value = int(magnitude % 256)  # Modulo 256 for ASCII range
            decoded_message.append(chr(ascii_value))

    return ''.join(decoded_message)

# ----------------- UI Navigation -----------------
def show_screen(screen_type):
    """Handles navigation between different steganography screens."""
    clear_main_content()
    if screen_type == "Text":
        text_steganography_screen()

# ----------------- Text Steganography -----------------
def text_steganography_screen():
    """Displays Text Steganography selection screen."""
    clear_main_content()

    ctk.CTkLabel(main_content, text="Text Steganography", font=("Arial", 30, "bold"), text_color="#FFFFFF").pack(pady=(50, 20))

    ctk.CTkButton(main_content, text="Encode", width=350, height=50, fg_color="#28a745", hover_color="#218838",
                  text_color="#ffffff", corner_radius=10, command=text_encode_screen).pack(pady=10)
    
    ctk.CTkButton(main_content, text="Decode", width=350, height=50, fg_color="#dc3545", hover_color="#c82333",
                  text_color="#ffffff", corner_radius=10, command=text_decode_screen).pack(pady=10)

# ----------------- Encoding Screen -----------------
def text_encode_screen():
    """Displays the screen for encoding text with Caesar Cipher."""
    global entry_message, entry_shift
    clear_main_content()

    ctk.CTkLabel(main_content, text="Encode Text", font=("Arial", 30, "bold"), text_color="#FFFFFF").pack(pady=(30, 20))

    entry_message = ctk.CTkTextbox(main_content, height=100, width=400, fg_color="#333333", text_color="#ffffff", corner_radius=10)
    entry_message.pack(pady=10)

    entry_shift = ctk.CTkEntry(main_content, placeholder_text="Enter shift for Caesar Cipher", width=400, fg_color="#333333", text_color="#ffffff", corner_radius=10)
    entry_shift.pack(pady=10)

    ctk.CTkButton(main_content, text="Save to File", width=350, height=40, fg_color="#007bff", hover_color="#0056b3",
                  text_color="#ffffff", corner_radius=10, command=save_encoded_text).pack(pady=10)

# ----------------- Decoding Screen -----------------
def text_decode_screen():
    """Displays the screen for decoding text with Caesar Cipher."""
    global entry_shift
    clear_main_content()

    ctk.CTkLabel(main_content, text="Decode Text", font=("Arial", 30, "bold"), text_color="#FFFFFF").pack(pady=(30, 20))

    entry_shift = ctk.CTkEntry(main_content, placeholder_text="Enter shift for Caesar Cipher", width=400, fg_color="#333333", text_color="#ffffff", corner_radius=10)
    entry_shift.pack(pady=10)

    ctk.CTkButton(main_content, text="Select File", width=350, height=40, fg_color="#ff8800", hover_color="#cc7000",
                  text_color="#ffffff", corner_radius=10, command=open_file_to_decode_text).pack(pady=10)

# ----------------- Encoding and Decoding Functions -----------------
def save_encoded_text():
    """Encrypts and saves the text to a file."""
    shift = get_shift_value()
    if shift is None:
        return

    secret_message = entry_message.get("1.0", "end-1c").strip()
    if not secret_message:
        messagebox.showerror("Input Error", "Please enter a message to encode.")
        return

    encrypted_message = caesar_cipher_encrypt(secret_message, shift)

    # Use spectratyping to encode the message into audio
    encode_message_with_spectratyping(encrypted_message)

def open_file_to_decode_text():
    """Opens an encrypted file and deciphers the message."""
    file_path = filedialog.askopenfilename(title="Select WAV File to Decode", filetypes=[("WAV Files", "*.wav")])
    if not file_path:
        return

    decrypted_message = decode_message_from_spectratyping(file_path)

    # Now decrypt the spectratyped message using Caesar cipher
    shift = get_shift_value()
    if shift is None:
        return

    final_decrypted_message = caesar_cipher_decrypt(decrypted_message, shift)

    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if save_path:
        with open(save_path, 'w') as output_file:
            output_file.write(final_decrypted_message)
        messagebox.showinfo("Decoding Complete", f"Decrypted text saved as {save_path}")

# ----------------- Sidebar Navigation -----------------
def create_sidebar():
    """Creates the navigation sidebar."""
    sidebar = ctk.CTkFrame(root, width=250, height=768, fg_color="#212121", corner_radius=15)
    sidebar.pack(side="left", fill="y", padx=10, pady=10)

    ctk.CTkLabel(sidebar, text="GRAPHY", font=("Arial", 24, "bold"), text_color="#FFFFFF").pack(pady=(20, 30))

    ctk.CTkButton(sidebar, text="Text", width=220, height=45, fg_color="#333333", hover_color="#444444",
                  text_color="#ffffff", corner_radius=20, command=lambda: show_screen("Text")).pack(pady=10)

    ctk.CTkButton(sidebar, text="Quit", width=220, height=45, fg_color="#333333", hover_color="#444444",
                  text_color="#ffffff", corner_radius=20, command=root.quit).pack(pady=10)

# Initialize Sidebar
create_sidebar()

# Start the UI
root.mainloop()
