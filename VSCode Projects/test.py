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

# Main menu screen
def main_menu_screen():
    clear_window()
    label = ctk.CTkLabel(root, text="Steganography Tool", font=("Roboto", 40, "bold"), fg_color="#ffffff", text_color="#4CAF50")
    label.pack(pady=40)

    btn_text = ctk.CTkButton(root, text="Text Steganography", width=250, height=45, fg_color="#4CAF50", hover_color="#45A049", command=lambda: get_shift_value_screen("Text"))
    btn_text.pack(pady=15)

    btn_image = ctk.CTkButton(root, text="Image Steganography", width=250, height=45, fg_color="#2196F3", hover_color="#1976D2", command=lambda: get_shift_value_screen("Image"))
    btn_image.pack(pady=15)

    btn_video = ctk.CTkButton(root, text="Video Steganography", width=250, height=45, fg_color="#FF5722", hover_color="#F44336", command=lambda: get_shift_value_screen("Video"))
    btn_video.pack(pady=15)

# Shift Value Screen
def get_shift_value_screen(steganography_type):
    clear_window()

    label = ctk.CTkLabel(root, text=f"Enter Caesar Cipher shift for {steganography_type} Steganography", font=("Roboto", 20, "bold"), fg_color="#ffffff", text_color="#2196F3")
    label.pack(pady=30)

    global entry_shift  # Use the global entry_shift widget
    entry_shift = ctk.CTkEntry(root, placeholder_text="Enter shift value", width=350, height=40)
    entry_shift.pack(pady=20)

    btn_continue = ctk.CTkButton(root, text="Continue", width=250, height=45, fg_color="#4CAF50", hover_color="#45A049", command=lambda: steganography_screen(steganography_type))
    btn_continue.pack(pady=20)

# Helper function to clear the window
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# General function to handle different steganography types
def steganography_screen(steganography_type):
    shift_value = get_shift_value()
    if shift_value is None:
        return  # Do nothing if the shift value is invalid

    if steganography_type == "Text":
        go_to_text_steganography(shift_value)
    elif steganography_type == "Image":
        go_to_image_steganography(shift_value)
    elif steganography_type == "Video":
        go_to_video_steganography(shift_value)

# Function for Text Steganography Screen
def go_to_text_steganography(shift_value):
    clear_window()
    label = ctk.CTkLabel(root, text="Text Steganography", font=("Roboto", 30, "bold"), fg_color="#ffffff", text_color="#FF5722")
    label.pack(pady=30)

    global entry_message
    entry_message = ctk.CTkTextbox(root, height=5, width=350)
    entry_message.pack(pady=20)

    btn_encode = ctk.CTkButton(root, text="Encode", width=250, height=45, fg_color="#4CAF50", hover_color="#45A049", command=lambda: encode_text_file(shift_value))
    btn_encode.pack(pady=15)

    btn_decode = ctk.CTkButton(root, text="Decode", width=250, height=45, fg_color="#FF9800", hover_color="#FF5722", command=lambda: decode_text_file(shift_value))
    btn_decode.pack(pady=15)

    btn_back = ctk.CTkButton(root, text="Back", width=250, height=45, fg_color="#9E9E9E", hover_color="#757575", command=main_menu_screen)
    btn_back.pack(pady=15)

# Function to encode text into a text file (Text Steganography)
def encode_text_file(shift_value):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        secret_message = entry_message.get("1.0", "end-1c")  # Get the secret message from the textbox
        encrypted_message = caesar_cipher_encrypt(secret_message, shift_value)
        with open(file_path, 'a') as file:
            file.write(encrypted_message)  # Append the encoded message to the file
        messagebox.showinfo("Success", "Message encoded in text file.")

# Function to decode text from a text file (Text Steganography)
def decode_text_file(shift_value):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            secret_message = file.read()
        decrypted_message = caesar_cipher_decrypt(secret_message, shift_value)
        messagebox.showinfo("Decoded Message", f"Decoded Message: {decrypted_message}")

# Function for Image Steganography Screen
def go_to_image_steganography(shift_value):
    clear_window()
    label = ctk.CTkLabel(root, text="Image Steganography", font=("Roboto", 30, "bold"), fg_color="#ffffff", text_color="#2196F3")
    label.pack(pady=30)

    # Select image to encode
    def encode_image_action():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            secret_message = entry_message.get("1.0", "end-1c")
            encoded_image_path = encode_image(file_path, secret_message)
            messagebox.showinfo("Success", f"Image saved at {encoded_image_path}")
    
    # Select image to decode
    def decode_image_action():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            decoded_message = decode_image(file_path)
            messagebox.showinfo("Decoded Message", f"Decoded Message: {decoded_message}")

    global entry_message
    entry_message = ctk.CTkTextbox(root, height=5, width=350)
    entry_message.pack(pady=20)

    btn_encode = ctk.CTkButton(root, text="Encode Image", width=250, height=45, fg_color="#4CAF50", hover_color="#45A049", command=encode_image_action)
    btn_encode.pack(pady=15)

    btn_decode = ctk.CTkButton(root, text="Decode Image", width=250, height=45, fg_color="#FF9800", hover_color="#FF5722", command=decode_image_action)
    btn_decode.pack(pady=15)

    btn_back = ctk.CTkButton(root, text="Back", width=250, height=45, fg_color="#9E9E9E", hover_color="#757575", command=main_menu_screen)
    btn_back.pack(pady=15)

# Function for Video Steganography Screen
def go_to_video_steganography(shift_value):
    clear_window()
    label = ctk.CTkLabel(root, text="Video Steganography", font=("Roboto", 30, "bold"), fg_color="#ffffff", text_color="#FF5722")
    label.pack(pady=30)

    # Select video to encode
    def encode_video_action():
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
        if file_path:
            secret_message = entry_message.get("1.0", "end-1c")
            encoded_video_path = encode_video_opencv(file_path, secret_message)
            messagebox.showinfo("Success", f"Video saved at {encoded_video_path}")
    
    # Select video to decode
    def decode_video_action():
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
        if file_path:
            decoded_message = decode_video_opencv(file_path)
            messagebox.showinfo("Decoded Message", f"Decoded Message: {decoded_message}")

    global entry_message
    entry_message = ctk.CTkTextbox(root, height=5, width=350)
    entry_message.pack(pady=20)

    btn_encode = ctk.CTkButton(root, text="Encode Video", width=250, height=45, fg_color="#4CAF50", hover_color="#45A049", command=encode_video_action)
    btn_encode.pack(pady=15)

    btn_decode = ctk.CTkButton(root, text="Decode Video", width=250, height=45, fg_color="#FF9800", hover_color="#FF5722", command=decode_video_action)
    btn_decode.pack(pady=15)

    btn_back = ctk.CTkButton(root, text="Back", width=250, height=45, fg_color="#9E9E9E", hover_color="#757575", command=main_menu_screen)
    btn_back.pack(pady=15)

# Create the main window
root = ctk.CTk()
root.title("Multimedia Steganography with Caesar Cipher")
root.geometry("1024x768")
root.configure(background="#2F2F2F")  # Dark background

# Create the initial screen (Main Menu)
main_menu_screen()

# Start the GUI
root.mainloop()
