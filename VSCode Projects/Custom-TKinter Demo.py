import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import cv2

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

# Function to encode text into an image (LSB Steganography)
def encode_image(image_path, secret_message):
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

# Function to decode text from an image (LSB Steganography)
def decode_image(image_path):
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
    secret_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    
    return secret_message

# Function to encode text into a text file (Text Steganography)
def encode_text_file(file_path, secret_message):
    with open(file_path, 'a') as file:
        file.write(secret_message)
    return file_path

# Function to decode text from a text file (Text Steganography)
def decode_text_file(file_path):
    with open(file_path, 'r') as file:
        secret_message = file.read()
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

# Main menu screen
def main_menu_screen():
    clear_window()
    label = ctk.CTkLabel(root, text="Choose the type of steganography", font=("Arial", 60))
    label.pack(pady=20)
    
    btn_text = ctk.CTkButton(root, text="Text Steganography", command=lambda: get_shift_value_screen("Text"))
    btn_text.pack(pady=10)
    
    btn_image = ctk.CTkButton(root, text="Image Steganography", command=lambda: get_shift_value_screen("Image"))
    btn_image.pack(pady=10)
    
    btn_video = ctk.CTkButton(root, text="Video Steganography", command=lambda: get_shift_value_screen("Video"))
    btn_video.pack(pady=10)

# Shift Value Screen
def get_shift_value_screen(steganography_type):
    clear_window()
    
    label = ctk.CTkLabel(root, text=f"Enter Caesar Cipher shift for {steganography_type} Steganography", font=("Arial", 20))
    label.pack(pady=20)
    
    global entry_shift  # Use the global entry_shift widget
    entry_shift = ctk.CTkEntry(root, placeholder_text="Enter shift value")
    entry_shift.pack(pady=10)
    
    btn_continue = ctk.CTkButton(root, text="Continue", command=lambda: steganography_screen(steganography_type))
    btn_continue.pack(pady=10)

# Handle which screen to show based on steganography type
def steganography_screen(steganography_type):
    shift_value = get_shift_value()
    if shift_value is None:
        return

    if steganography_type == "Text":
        go_to_text_steganography(shift_value)
    elif steganography_type == "Image":
        go_to_image_steganography(shift_value)
    elif steganography_type == "Video":
        go_to_video_steganography(shift_value)

# Text Steganography Screen
def go_to_text_steganography(shift_value):
    clear_window()
    
    label = ctk.CTkLabel(root, text="Text Steganography", font=("Arial", 20))
    label.pack(pady=20)
    
    # Add entry widget for secret message
    global entry_message
    entry_message = ctk.CTkEntry(root, placeholder_text="Enter secret message")
    entry_message.pack(pady=10)

    btn_encode = ctk.CTkButton(root, text="Encode", command=lambda: encode_text(shift_value))
    btn_encode.pack(pady=10)
    
    btn_decode = ctk.CTkButton(root, text="Decode", command=lambda: decode_text(shift_value))
    btn_decode.pack(pady=10)
    
    btn_back = ctk.CTkButton(root, text="Back", command=main_menu_screen)
    btn_back.pack(pady=10)

# Encoding and Decoding Methods for Text
def encode_text(shift_value):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        secret_message = entry_message.get()
        encrypted_message = caesar_cipher_encrypt(secret_message, shift_value)
        encode_text_file(file_path, encrypted_message)
        messagebox.showinfo("Success", "Message encoded in text file.")

def decode_text(shift_value):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        decrypted_message = decode_text_file(file_path)
        secret_message = caesar_cipher_decrypt(decrypted_message, shift_value)
        messagebox.showinfo("Decoded Message", secret_message)

# Image Steganography Screen
def go_to_image_steganography(shift_value):
    clear_window()
    
    label = ctk.CTkLabel(root, text="Image Steganography", font=("Arial", 20))
    label.pack(pady=20)
    
    # Add entry widget for secret message
    global entry_message
    entry_message = ctk.CTkEntry(root, placeholder_text="Enter secret message")
    entry_message.pack(pady=10)

    btn_encode = ctk.CTkButton(root, text="Encode", command=lambda: encode_image_method(shift_value))
    btn_encode.pack(pady=10)
    
    btn_decode = ctk.CTkButton(root, text="Decode", command=lambda: decode_image_method(shift_value))
    btn_decode.pack(pady=10)
    
    btn_back = ctk.CTkButton(root, text="Back", command=main_menu_screen)
    btn_back.pack(pady=10)

# Encoding and Decoding Methods for Image
def encode_image_method(shift_value):
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png;.jpg;*.jpeg")])
    if image_path:
        secret_message = entry_message.get()
        encrypted_message = caesar_cipher_encrypt(secret_message, shift_value)
        output = encode_image(image_path, encrypted_message)
        messagebox.showinfo("Success", f"Message encoded in image: {output}")

def decode_image_method(shift_value):
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png;.jpg;*.jpeg")])
    if image_path:
        encrypted_message = decode_image(image_path)
        secret_message = caesar_cipher_decrypt(encrypted_message, shift_value)
        messagebox.showinfo("Decoded Message", secret_message)

# Video Steganography Screen
def go_to_video_steganography(shift_value):
    clear_window()
    
    label = ctk.CTkLabel(root, text="Video Steganography", font=("Arial", 20))
    label.pack(pady=20)
    
    # Add entry widget for secret message
    global entry_message
    entry_message = ctk.CTkEntry(root, placeholder_text="Enter secret message")
    entry_message.pack(pady=10)

    btn_encode = ctk.CTkButton(root, text="Encode", command=lambda: encode_video_method(shift_value))
    btn_encode.pack(pady=10)
    
    btn_decode = ctk.CTkButton(root, text="Decode", command=lambda: decode_video_method(shift_value))
    btn_decode.pack(pady=10)
    
    btn_back = ctk.CTkButton(root, text="Back", command=main_menu_screen)
    btn_back.pack(pady=10)

# Encoding and Decoding Methods for Video
def encode_video_method(shift_value):
    video_path = filedialog.askopenfilename(filetypes=[("Video Files", ".mp4;.avi")])
    if video_path:
        secret_message = entry_message.get()
        encrypted_message = caesar_cipher_encrypt(secret_message, shift_value)
        output = encode_video_opencv(video_path, encrypted_message)
        messagebox.showinfo("Success", f"Message encoded in video: {output}")

def decode_video_method(shift_value):
    video_path = filedialog.askopenfilename(filetypes=[("Video Files", ".mp4;.avi")])
    if video_path:
        encrypted_message = decode_video_opencv(video_path)
        secret_message = caesar_cipher_decrypt(encrypted_message, shift_value)
        messagebox.showinfo("Decoded Message", secret_message)

# Helper function to clear the window
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Initialize the GUI
root = ctk.CTk()

root.title("Multimedia Steganography with Caesar Cipher")
root.geometry("1024x768")
root.configure(background="#F2F2F2")

# Create the initial screen (Main Menu)
main_menu_screen()

# Start the GUI
root.mainloop()
