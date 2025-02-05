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

from PIL import Image

def encode_image(image_path, secret_message):
    try:
        image = Image.open(image_path)
        binary_message = ''.join(format(ord(i), '08b') for i in secret_message) + '1111111111111110'
        pixels = image.load()
        width, height = image.size
        data_index = 0

        for y in range(height):
            for x in range(width):
                pixel = list(pixels[x, y])
                for i in range(3):
                    if data_index < len(binary_message):
                        pixel[i] = pixel[i] & 254 | int(binary_message[data_index])
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
                for i in range(3):
                    binary_message += str(pixel[i] & 1)

        binary_message = binary_message.split('1111111111111110')[0]
        secret_message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))

        return secret_message
    except Exception as e:
        raise Exception(f"Error decoding image: {e}")

import cv2

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

def get_shift_value():
    while True:
        try:
            shift = int(input("Enter shift value: "))
            return shift
        except ValueError:
            print("Invalid input. Please enter an integer.")

import ttkbootstrap as tb
from tkinter import filedialog, Text
import tkinter as tk

class GraphyApp(tb.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("GRAPHY - Steganography App")
        self.geometry("800x500")

        # Sidebar Frame
        self.sidebar = tb.Frame(self, bootstyle="dark", width=200)
        self.sidebar.pack(side="left", fill="y")

        # Sidebar Buttons
        self.btn_text = tb.Button(self.sidebar, text="Text Steganography", command=self.show_text_screen, bootstyle="secondary")
        self.btn_text.pack(pady=10, fill="x")

        self.btn_image = tb.Button(self.sidebar, text="Image Steganography", command=self.show_image_screen, bootstyle="secondary")
        self.btn_image.pack(pady=10, fill="x")

        self.btn_video = tb.Button(self.sidebar, text="Video Steganography", command=self.show_video_screen, bootstyle="secondary")
        self.btn_video.pack(pady=10, fill="x")

        # Main Frame
        self.main_frame = tb.Frame(self, bootstyle="dark")
        self.main_frame.pack(side="right", expand=True, fill="both")

        # Default Screen
        self.show_welcome_screen()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        self.clear_main_frame()
        tb.Label(self.main_frame, text="Welcome to GRAPHY", font=("Helvetica", 20), bootstyle="inverse-light").pack(pady=20)
        tb.Button(self.main_frame, text="Get Started", command=self.show_text_screen, bootstyle="primary").pack(pady=10)

    def show_text_screen(self):
        self.clear_main_frame()
        tb.Label(self.main_frame, text="Text Steganography", font=("Helvetica", 16), bootstyle="inverse-light").pack(pady=10)
        tb.Label(self.main_frame, text="Enter text:", bootstyle="light").pack()
        
        text_input = Text(self.main_frame, height=5, width=50)
        text_input.pack(pady=5)

        tb.Button(self.main_frame, text="Select File", command=self.select_file, bootstyle="primary").pack(pady=5)
        tb.Button(self.main_frame, text="Encode", bootstyle="success").pack(pady=5)
        tb.Button(self.main_frame, text="Decode", bootstyle="danger").pack(pady=5)

    def show_image_screen(self):
        self.clear_main_frame()
        tb.Label(self.main_frame, text="Image Steganography", font=("Helvetica", 16), bootstyle="inverse-light").pack(pady=10)
        tb.Button(self.main_frame, text="Select Image", command=self.select_file, bootstyle="primary").pack(pady=10)
        tb.Button(self.main_frame, text="Encode", bootstyle="success").pack(pady=5)
        tb.Button(self.main_frame, text="Decode", bootstyle="danger").pack(pady=5)

    def show_video_screen(self):
        self.clear_main_frame()
        tb.Label(self.main_frame, text="Video Steganography", font=("Helvetica", 16), bootstyle="inverse-light").pack(pady=10)
        tb.Button(self.main_frame, text="Select Video", command=self.select_file, bootstyle="primary").pack(pady=10)
        tb.Button(self.main_frame, text="Encode", bootstyle="success").pack(pady=5)
        tb.Button(self.main_frame, text="Decode", bootstyle="danger").pack(pady=5)

    def select_file(self):
        filedialog.askopenfilename()

if __name__ == "__main__":
    app = GraphyApp()
    app.mainloop()
