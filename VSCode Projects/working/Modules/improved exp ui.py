import customtkinter as ctk
import os
from tkinter import filedialog, messagebox
from PIL import Image
import cv2

# Set appearance mode to dark
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")  # Default dark color palette

# --- Caesar Cipher Functions ---
def caesar_cipher_encrypt(plaintext, shift):
    if not isinstance(shift, int):
        raise ValueError("Shift value must be an integer.")
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
    return caesar_cipher_encrypt(ciphertext, -shift)


# --- Text Steganography Functions ---
def encode_text_file(file_path, secret_message):
    try:
        with open(file_path, 'a') as file:
            file.write(secret_message)
        return file_path
    except Exception as e:
        raise Exception(f"Error encoding text to file: {e}")

def decode_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            secret_message = file.read()
        return secret_message
    except Exception as e:
        raise Exception(f"Error decoding text from file: {e}")


# --- Image Steganography Functions ---
def encode_image(image_path, secret_message):
    try:
        image = Image.open(image_path)
        binary_message = ''.join(format(ord(i), '08b') for i in secret_message) + '1111111111111110'  # Add stop delimiter
        pixels = image.load()
        width, height = image.size
        data_index = 0

        for y in range(height):
            for x in range(width):
                pixel = list(pixels[x, y])
                for i in range(3):  # RGB channels
                    if data_index < len(binary_message):
                        pixel[i] = pixel[i] & 254 | int(binary_message[data_index])  # Change the LSB
                        data_index += 1
                pixels[x, y] = tuple(pixel)

        output_path = 'encoded_image.png'
        image.save(output_path)
        return output_path
    except Exception as e:
        raise Exception(f"Error encoding image: {e}")

def decode_image(image_path):
    try:
        image = Image.open(image_path)
        binary_message = ""
        pixels = image.load()
        width, height = image.size

        for y in range(height):
            for x in range(width):
                pixel = list(pixels[x, y])
                for i in range(3):  # RGB channels
                    binary_message += str(pixel[i] & 1)  # Extract the LSB

        binary_message = binary_message.split('1111111111111110')[0]  # Stop delimiter
        secret_message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))

        return secret_message
    except Exception as e:
        raise Exception(f"Error decoding image: {e}")


# --- Video Steganography Functions ---
def encode_video_opencv(video_path, secret_message):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("Error opening video file.")

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        out = cv2.VideoWriter('encoded_video_opencv.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
        binary_message = ''.join(format(ord(i), '08b') for i in secret_message) + '1111111111111110'
        message_index = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            for y in range(frame_height):
                for x in range(frame_width):
                    if message_index < len(binary_message):
                        pixel = frame[y, x]
                        for c in range(3):
                            if message_index < len(binary_message):
                                pixel[c] = pixel[c] & 0xFE | int(binary_message[message_index])
                                message_index += 1
                        frame[y, x] = pixel
            out.write(frame)

        cap.release()
        out.release()
        return 'encoded_video_opencv.mp4'
    except Exception as e:
        raise Exception(f"Error encoding video: {e}")

def decode_video_opencv(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("Error opening video file.")

        binary_message = ""
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            for y in range(frame.shape[0]):
                for x in range(frame.shape[1]):
                    pixel = frame[y, x]
                    for c in range(3):
                        binary_message += str(pixel[c] & 1)

        cap.release()
        binary_message = binary_message.split('1111111111111110')[0]
        secret_message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))

        return secret_message
    except Exception as e:
        raise Exception(f"Error decoding video: {e}")


# --- Utility Functions ---
def get_shift_value(entry_shift):
    shift_str = entry_shift.get()
    if not shift_str.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid integer for the Caesar Cipher shift.")
        return None
    return int(shift_str)

import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter.font as tkfont  # For custom font support

# Set appearance
ctk.set_appearance_mode("dark")  # Dark mode 
ctk.set_default_color_theme("dark-blue")

# Theme colors
DARK_BG = "#121212"  # Dark background color
LIGHT_BG = "#F5F5F5"  # Light background for minimalism
ACCENT_COLOR = "#00ADB5"  # Soft cyan for accents
TEXT_COLOR = "#E0E0E0"  # Light grey text color for contrast

# Google Product Sans Font (make sure it's installed on the system)
PRODUCT_SANS = "Product Sans"

class GraphyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window properties
        self.title("GRAPHY - Steganography Tool")
        self.geometry("1280x720")
        self.configure(bg=DARK_BG)

        # Sidebar state
        self.sidebar_expanded = False

        # Sidebar Frame (Hidden Initially)
        self.sidebar = ctk.CTkFrame(self, width=10, height=1000, corner_radius=12, fg_color="#1e1e1e")
        self.sidebar.place(x=0, y=0)

        # Sidebar Toggle Button
        self.sidebar_toggle_btn = ctk.CTkButton(
            self.sidebar, text="☰", command=self.toggle_sidebar, fg_color="transparent", text_color="white",
            font=(PRODUCT_SANS, 20, "bold"), hover_color="#333333", width=50
        )
        self.sidebar_toggle_btn.place(x=190, y=65)

        # Sidebar Buttons (For Steganography Options)
        self.steg_types = [
            ("📝 Text", self.select_text_steganography),
            ("🖼 Image", self.select_image_steganography),
            ("🎥 Video", self.select_video_steganography)
        ]

        self.sidebar_buttons = []
        for idx, (label, command) in enumerate(self.steg_types):
            btn = ctk.CTkButton(
                self.sidebar, text=label, command=command, fg_color="transparent", text_color="white",
                font=(PRODUCT_SANS, 16), hover_color="#333333", width=200, height=40
            )
            btn.place(x=10, y=80 + (idx * 60))
            self.sidebar_buttons.append(btn)

        # Add Theme Toggle Button to Sidebar
        self.theme_toggle_btn = ctk.CTkButton(
            self.sidebar, text="🌙", command=self.toggle_theme, fg_color="transparent", text_color="white",
            font=(PRODUCT_SANS, 18)
        )
        self.theme_toggle_btn.place(x=10, y=80 + (len(self.steg_types) * 60) + 20)  # Place it below the steganography options

        # Header Frame
        self.header = ctk.CTkFrame(self, fg_color=DARK_BG, height=60)
        self.header.pack(fill="x")

        # Header Label
        self.header_label = ctk.CTkLabel(self.header, text="Welcome to GRAPHY!", font=(PRODUCT_SANS, 24, "bold"), text_color="white")
        self.header_label.place(x=20, y=15)

        # Display Home Screen
        self.show_home()

    def show_home(self):
        self.clear_main()

        # Set header label to indicate the screen
        self.header_label.configure(text="Welcome to GRAPHY!")

        # Remove transparent background and use the main window
        welcome_text = ctk.CTkLabel(self, text="GRAPHY!", font=(PRODUCT_SANS, 28, "bold"), text_color=TEXT_COLOR)
        welcome_text.place(relx=0.5, rely=0.4, anchor="center")  # Centered

        # Get Started button with sleek styling
        get_started_btn = ctk.CTkButton(self, text="🚀 Get Started", command=self.toggle_sidebar, fg_color=ACCENT_COLOR, hover_color="#007B83", font=(PRODUCT_SANS, 20))
        get_started_btn.place(relx=0.5, rely=0.5, anchor="center")

    def toggle_sidebar(self):
        """Smoothly Expands or Collapses the Sidebar"""
        if self.sidebar_expanded:
            self.sidebar.place_configure(width=10)
            for btn in self.sidebar_buttons:
                btn.place_forget()
            self.theme_toggle_btn.place_forget()
        else:
            self.sidebar.place_configure(width=250)
            for idx, btn in enumerate(self.sidebar_buttons):
                btn.place(x=10, y=80 + (idx * 60))
            self.theme_toggle_btn.place(x=10, y=80 + (len(self.steg_types) * 60) + 20)

        self.sidebar_expanded = not self.sidebar_expanded

    def toggle_theme(self):
        """Switches Between Light and Dark Mode"""
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("Light")
            self.configure(bg=LIGHT_BG)
            self.sidebar.configure(fg_color="#E0E0E0")
            self.header.configure(fg_color="white")
            self.theme_toggle_btn.configure(text="🌞")
        else:
            ctk.set_appearance_mode("Dark")
            self.configure(bg=DARK_BG)
            self.sidebar.configure(fg_color="#333333")
            self.header.configure(fg_color=DARK_BG)
            self.theme_toggle_btn.configure(text="🌙")

    def select_text_steganography(self):
        """Text Steganography Selection"""
        self.show_steganography_ui("Text Steganography")

    def select_image_steganography(self):
        """Image Steganography Selection"""
        self.show_steganography_ui("Image Steganography")

    def select_video_steganography(self):
        """Video Steganography Selection"""
        self.show_steganography_ui("Video Steganography")

    def show_steganography_ui(self, steg_type):
        """Displays Steganography Encode/Decode UI"""
        self.clear_main()
        self.header_label.configure(text=steg_type)

        encode_btn = ctk.CTkButton(self, text="Encode", fg_color=ACCENT_COLOR, hover_color="#007B83", font=(PRODUCT_SANS, 18))
        encode_btn.place(relx=0.5, rely=0.4, anchor="center")

        decode_btn = ctk.CTkButton(self, text="Decode", fg_color=ACCENT_COLOR, hover_color="#007B83", font=(PRODUCT_SANS, 18))
        decode_btn.place(relx=0.5, rely=0.5, anchor="center")

    def clear_main(self):
        """Clears Main Frame"""
        for widget in self.winfo_children():
            widget.destroy()

# Run the App
if __name__ == "__main__":
    app = GraphyApp()
    app.mainloop()
