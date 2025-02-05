import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import cv2
import time

# Set appearance mode before creating UI elements
ctk.set_appearance_mode("dark")

# Initialize the main window
root = ctk.CTk()
root.title("GRAPHY")
root.geometry("1024x768")
root.configure(bg="#1e1e1e")

# Global variable to store the main content frame
main_content = None

# Caesar Cipher Encryption and Decryption Functions
def caesar_cipher_encrypt(plaintext, shift):
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

# General Encoding and Decoding Functions for LSB
def encode_message_in_pixels(pixels, width, height, binary_message):
    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])
            for i in range(3):  # RGB channels
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & 254 | int(binary_message[data_index])  # Change the LSB
                    data_index += 1
            pixels[x, y] = tuple(pixel)

def decode_message_from_pixels(pixels, width, height):
    binary_message = ""
    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])
            for i in range(3):  # RGB channels
                binary_message += str(pixel[i] & 1)  # Extract the LSB
    return binary_message

# Function to encode text into an image (LSB Steganography)
def encode_image(image_path, secret_message):
    image = Image.open(image_path)
    binary_message = ''.join(format(ord(i), '08b') for i in secret_message) + '1111111111111110'  # Add stop delimiter
    pixels = image.load()
    width, height = image.size
    encode_message_in_pixels(pixels, width, height, binary_message)
    output_path = 'encoded_image.png'
    image.save(output_path)
    return output_path

# Function to decode text from an image (LSB Steganography)
def decode_image(image_path):
    image = Image.open(image_path)
    pixels = image.load()
    width, height = image.size
    binary_message = decode_message_from_pixels(pixels, width, height)
    
    # Split the message at the delimiter '1111111111111110' (the end of the hidden message)
    binary_message = binary_message.split('1111111111111110')[0]
    secret_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    
    return secret_message

# Function to encode text into a video using OpenCV (Video Steganography)
def encode_video_opencv(video_path, secret_message):
    cap = cv2.VideoCapture(video_path)  # Open the video file
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Create VideoWriter object to save the encoded video
    out = cv2.VideoWriter('encoded_video_opencv.mp4', 
                          cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    binary_message = ''.join(format(ord(i), '08b') for i in secret_message) + '1111111111111110'  # Add stop delimiter
    message_index = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # If no frame is read, break the loop

        # Iterate over the pixels in the frame and embed the message
        for y in range(frame_height):
            for x in range(frame_width):
                if message_index < len(binary_message):
                    pixel = frame[y, x]
                    for c in range(3):  # RGB channels
                        if message_index < len(binary_message):
                            pixel[c] = pixel[c] & 0xFE | int(binary_message[message_index])  # Change the LSB
                            message_index += 1
                    frame[y, x] = pixel

        out.write(frame)  # Write the frame to the output video

    cap.release()
    out.release()
    return 'encoded_video_opencv.mp4'

# Function to decode text from a video using OpenCV (Video Steganography)
def decode_video_opencv(video_path):
    cap = cv2.VideoCapture(video_path)
    binary_message = ""
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # If no frame is read, break the loop

        for y in range(frame.shape[0]):
            for x in range(frame.shape[1]):
                pixel = frame[y, x]
                for c in range(3):  # RGB channels
                    binary_message += str(pixel[c] & 1)  # Extract the LSB
    
    cap.release()
    
    # Split the message at the delimiter '1111111111111110' (the end of the hidden message)
    binary_message = binary_message.split('1111111111111110')[0]
    secret_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    
    return secret_message

# Helper function to validate the Caesar Cipher shift
def get_shift_value():
    shift_str = entry_shift.get()
    if not shift_str.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid integer for the Caesar Cipher shift.")
        return None
    return int(shift_str)

# Function to create sidebar navigation with modern look
def create_sidebar():
    sidebar = ctk.CTkFrame(root, width=250, height=768, fg_color="#212121", corner_radius=15)  # Rounded corners for sidebar
    sidebar.pack(side="left", fill="y", padx=10, pady=10)

    label = ctk.CTkLabel(sidebar, text="GRAPHY", font=("Arial", 24, "bold"), text_color="#FFFFFF")
    label.pack(pady=(20, 30))

    # Modern buttons with rounded corners and hover effects
    btn_text = ctk.CTkButton(sidebar, text="Text", width=220, height=45, fg_color="#333333", hover_color="#444444", text_color="#ffffff", corner_radius=20, command=lambda: show_screen("Text"))
    btn_text.pack(pady=10)

    btn_image = ctk.CTkButton(sidebar, text="Image", width=220, height=45, fg_color="#333333", hover_color="#444444", text_color="#ffffff", corner_radius=20, command=lambda: show_screen("Image"))
    btn_image.pack(pady=10)

    btn_video = ctk.CTkButton(sidebar, text="Video", width=220, height=45, fg_color="#333333", hover_color="#444444", text_color="#ffffff", corner_radius=20, command=lambda: show_screen("Video"))
    btn_video.pack(pady=10)

    btn_quit = ctk.CTkButton(sidebar, text="Quit", width=220, height=45, fg_color="#333333", hover_color="#444444", text_color="#ffffff", corner_radius=20, command=root.quit)
    btn_quit.pack(pady=10)

# Function to add modern gradient background to main content area
def add_gradient_background(frame):
    gradient_color1 = "#000000"
    gradient_color2 = "#212121"
    frame.configure(fg_color=[gradient_color1, gradient_color2])  # Apply gradient background

# Function to display the selected screen (Text, Image, or Video)
def show_screen(screen_type):
    clear_main_content()

    if screen_type == "Text":
        go_to_text_steganography()
    elif screen_type == "Image":
        go_to_image_steganography()
    elif screen_type == "Video":
        go_to_video_steganography()

# Function to clear the main content area
def clear_main_content():
    if main_content:  # Check if main_content is defined
        for widget in main_content.winfo_children():
            widget.destroy()

# Function for Text Steganography Screen with modern styling
def go_to_text_steganography():
    label = ctk.CTkLabel(main_content, text="Text Steganography", font=("Arial", 30, "bold"), text_color="#FFFFFF")
    label.pack(pady=(50, 20))

    global entry_message
    entry_message = ctk.CTkTextbox(main_content, height=5, width=350, fg_color="#333333", text_color="#ffffff", corner_radius=10)
    entry_message.pack(pady=10)

    global entry_shift
    entry_shift = ctk.CTkEntry(main_content, placeholder_text="Enter shift for Caesar Cipher", width=350, fg_color="#333333", text_color="#ffffff", corner_radius=10)
    entry_shift.pack(pady=10)

    encrypt_btn = ctk.CTkButton(main_content, text="Encrypt", width=350, height=40, fg_color="#28a745", hover_color="#218838", text_color="#ffffff", corner_radius=10, command=encrypt_text)
    encrypt_btn.pack(pady=5)

    decrypt_btn = ctk.CTkButton(main_content, text="Decrypt", width=350, height=40, fg_color="#dc3545", hover_color="#c82333", text_color="#ffffff", corner_radius=10, command=decrypt_text)
    decrypt_btn.pack(pady=5)

# Function to encrypt text using Caesar Cipher
def encrypt_text():
    secret_message = entry_message.get("1.0", "end-1c")
    shift = get_shift_value()
    if secret_message and shift is not None:
        encrypted_message = caesar_cipher_encrypt(secret_message, shift)
        entry_message.delete("1.0", "end")
        entry_message.insert("1.0", encrypted_message)

# Function to decrypt text using Caesar Cipher
def decrypt_text():
    secret_message = entry_message.get("1.0", "end-1c")
    shift = get_shift_value()
    if secret_message and shift is not None:
        decrypted_message = caesar_cipher_decrypt(secret_message, shift)
        entry_message.delete("1.0", "end")
        entry_message.insert("1.0", decrypted_message)

# Functions for Image Steganography
def open_file_to_encode_image():
    file_path = filedialog.askopenfilename(title="Select Image to Encode", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        secret_message = entry_message.get("1.0", "end-1c")
        if secret_message:
            encoded_file = encode_image(file_path, secret_message)
            messagebox.showinfo("Encoding Complete", f"Image saved as {encoded_file}")

def open_file_to_decode_image():
    file_path = filedialog.askopenfilename(title="Select Encoded Image to Decode", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        secret_message = decode_image(file_path)
        entry_message.delete("1.0", "end")
        entry_message.insert("1.0", secret_message)
        messagebox.showinfo("Decoding Complete", "Message successfully decoded!")

def go_to_image_steganography():
    label = ctk.CTkLabel(main_content, text="Image Steganography", font=("Arial", 30, "bold"), text_color="#FFFFFF")
    label.pack(pady=(50, 20))

    encode_btn = ctk.CTkButton(main_content, text="Encode Image", width=350, height=40, fg_color="#28a745", hover_color="#218838", text_color="#ffffff", corner_radius=10, command=open_file_to_encode_image)
    encode_btn.pack(pady=5)

    decode_btn = ctk.CTkButton(main_content, text="Decode Image", width=350, height=40, fg_color="#dc3545", hover_color="#c82333", text_color="#ffffff", corner_radius=10, command=open_file_to_decode_image)
    decode_btn.pack(pady=5)

# Functions for Video Steganography
def open_file_to_encode_video():
    file_path = filedialog.askopenfilename(title="Select Video to Encode", filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
    if file_path:
        secret_message = entry_message.get("1.0", "end-1c")
        if secret_message:
            encoded_file = encode_video_opencv(file_path, secret_message)
            messagebox.showinfo("Encoding Complete", f"Video saved as {encoded_file}")

def open_file_to_decode_video():
    file_path = filedialog.askopenfilename(title="Select Encoded Video to Decode", filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
    if file_path:
        secret_message = decode_video_opencv(file_path)
        entry_message.delete("1.0", "end")
        entry_message.insert("1.0", secret_message)
        messagebox.showinfo("Decoding Complete", "Message successfully decoded!")

def go_to_video_steganography():
    label = ctk.CTkLabel(main_content, text="Video Steganography", font=("Arial", 30, "bold"), text_color="#FFFFFF")
    label.pack(pady=(50, 20))

    encode_btn = ctk.CTkButton(main_content, text="Encode Video", width=350, height=40, fg_color="#28a745", hover_color="#218838", text_color="#ffffff", corner_radius=10, command=open_file_to_encode_video)
    encode_btn.pack(pady=5)

    decode_btn = ctk.CTkButton(main_content, text="Decode Video", width=350, height=40, fg_color="#dc3545", hover_color="#c82333", text_color="#ffffff", corner_radius=10, command=open_file_to_decode_video)
    decode_btn.pack(pady=5)

# Initialize Sidebar and Main Content Area
create_sidebar()
main_content = ctk.CTkFrame(root)
main_content.pack(side="right", fill="both", expand=True, padx=10, pady=10)
add_gradient_background(main_content)

# Start the UI
root.mainloop()
