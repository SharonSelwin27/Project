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

class GraphyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GRAPHY - Steganography Tool")
        self.geometry("900x600")
        self.configure(bg="black")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Sidebar (Hidden initially)
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="gray20")
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")
        self.sidebar.grid_rowconfigure(2, weight=1)

        # App Name in Sidebar
        self.app_label = ctk.CTkLabel(self.sidebar, text="GRAPHY", font=("Product Sans", 20, "bold"))
        self.app_label.grid(row=0, column=0, padx=20, pady=20)

        # Steganography Types (Secondary Frame)
        self.options_frame = ctk.CTkFrame(self.sidebar, fg_color="gray15")
        self.options_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.steg_types = ["Text Steganography", "Image Steganography", "Video Steganography"]
        for idx, steg in enumerate(self.steg_types):
            btn = ctk.CTkButton(self.options_frame, text=steg, command=lambda s=steg: self.select_steganography(s))
            btn.grid(row=idx, column=0, padx=10, pady=5, sticky="ew")

        # Bottom Navigation Buttons
        self.home_btn = ctk.CTkButton(self.sidebar, text="Home", command=self.show_home, fg_color="gray30")
        self.home_btn.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        self.quit_btn = ctk.CTkButton(self.sidebar, text="Quit", command=self.quit, fg_color="red")
        self.quit_btn.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # Header
        self.header = ctk.CTkLabel(self, text="Welcome to GRAPHY", font=("Product Sans", 18, "bold"), fg_color="gray10", height=50)
        self.header.grid(row=0, column=1, sticky="ew")

        # Main Content Frame
        self.main_frame = ctk.CTkFrame(self, fg_color="gray10")
        self.main_frame.grid(row=1, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Welcome Screen
        self.show_home()

    def show_home(self):
        """Displays the Home Screen"""
        self.clear_main()
        self.header.configure(text="Welcome to GRAPHY")
        self.get_started_btn = ctk.CTkButton(self.main_frame, text="Get Started", command=self.show_sidebar)
        self.get_started_btn.pack(pady=20)

    def show_sidebar(self):
        """Reveals Sidebar"""
        self.sidebar.grid()
        self.show_home()

    def select_steganography(self, steg_type):
        """Displays Steganography Options"""
        self.clear_main()
        self.header.configure(text=steg_type)
        self.selected_steg = steg_type

        # Encode & Decode Buttons
        self.encode_btn = ctk.CTkButton(self.main_frame, text="Encode", command=lambda: self.show_process("Encode"))
        self.encode_btn.pack(pady=10)

        self.decode_btn = ctk.CTkButton(self.main_frame, text="Decode", command=lambda: self.show_process("Decode"))
        self.decode_btn.pack(pady=10)

    def show_process(self, action):
        """Displays input and file selection UI based on steganography type"""
        self.clear_main()
        self.header.configure(text=f"{self.selected_steg} - {action}")

        # Input Text Box
        self.input_text = ctk.CTkEntry(self.main_frame, placeholder_text="Enter text to encode/decode", width=400)
        self.input_text.pack(pady=10)

        # Shift Value Input Box
        self.shift_label = ctk.CTkLabel(self.main_frame, text="Enter Shift Value (for Cipher Text):")
        self.shift_label.pack(pady=(10, 0))
        
        self.shift_value = ctk.CTkEntry(self.main_frame, placeholder_text="Shift Value (e.g., 3)", width=100)
        self.shift_value.pack(pady=5)

        # File Selection
        file_btn_text = "Select File"
        file_action = self.select_file

        if "Text" in self.selected_steg:
            file_btn_text = "Select Text File"
        elif "Image" in self.selected_steg:
            file_btn_text = "Select Image"
        elif "Video" in self.selected_steg:
            file_btn_text = "Select Video"

        self.file_button = ctk.CTkButton(self.main_frame, text=file_btn_text, command=file_action)
        self.file_button.pack(pady=10)

        # Show only the relevant button (Encode or Decode)
        if action == "Encode":
            self.process_encode_btn = ctk.CTkButton(self.main_frame, text="Encode", command=self.encode_data, fg_color="green")
            self.process_encode_btn.pack(pady=10)
        elif action == "Decode":
            self.process_decode_btn = ctk.CTkButton(self.main_frame, text="Decode", command=self.decode_data, fg_color="blue")
            self.process_decode_btn.pack(pady=10)

    def select_file(self):
        """Handles File Selection"""
        file_types = [("All Files", "*.*")]
        if "Text" in self.selected_steg:
            file_types = [("Text Files", "*.txt")]
        elif "Image" in self.selected_steg:
            file_types = [("Image Files", "*.png;*.jpg;*.jpeg")]
        elif "Video" in self.selected_steg:
            file_types = [("Video Files", "*.mp4")]

        file_path = filedialog.askopenfilename(title="Select File", filetypes=file_types)
        if file_path:
            messagebox.showinfo("File Selected", f"Selected File: {file_path}")

    def encode_data(self):
        """Placeholder function for encoding"""
        shift = self.shift_value.get()
        if not shift.isdigit():
            messagebox.showerror("Invalid Input", "Shift value must be a number!")
            return

        messagebox.showinfo("Encoding", f"Encoding with shift: {shift}")

    def decode_data(self):
        """Placeholder function for decoding"""
        shift = self.shift_value.get()
        if not shift.isdigit():
            messagebox.showerror("Invalid Input", "Shift value must be a number!")
            return

        messagebox.showinfo("Decoding", f"Decoding with shift: {shift}")

    def clear_main(self):
        """Clears Main Frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# Run the App
if __name__ == "__main__":
    app = GraphyApp()
    app.mainloop()
