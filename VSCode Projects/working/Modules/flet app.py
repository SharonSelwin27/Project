import flet as ft
from tkinter import filedialog, messagebox
from PIL import Image
import cv2

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


# --- Flet GUI Functions ---
def encode_data(page, input_text, shift_value, file_button, selected_steg):
    shift = shift_value.value
    if not shift.isdigit():
        page.add(ft.Text("Shift value must be a number!", color="red"))
        return

    page.add(ft.Text(f"Encoding with shift: {shift}"))
    # Logic for encoding based on selected steganography type


def decode_data(page, input_text, shift_value, file_button, selected_steg):
    shift = shift_value.value
    if not shift.isdigit():
        page.add(ft.Text("Shift value must be a number!", color="red"))
        return

    page.add(ft.Text(f"Decoding with shift: {shift}"))
    # Logic for decoding based on selected steganography type


def main(page):
    page.title = "GRAPHY - Steganography Tool"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # App Layout
    app_label = ft.Text("GRAPHY", size=24, weight=ft.FontWeight.BOLD)
    options_frame = ft.Column()
    steg_types = ["Text Steganography", "Image Steganography", "Video Steganography"]

    def on_steg_type_select(selected_steg):
        page.add(ft.Text(f"Selected Steganography: {selected_steg}"))

        # Show encoding/decoding options
        input_text = ft.TextField(label="Enter text to encode/decode")
        shift_value = ft.TextField(label="Enter Shift Value (for Cipher Text)", value="3")
        file_button = ft.FilePicker()
        
        encode_button = ft.ElevatedButton(text="Encode", on_click=lambda _: encode_data(page, input_text, shift_value, file_button, selected_steg))
        decode_button = ft.ElevatedButton(text="Decode", on_click=lambda _: decode_data(page, input_text, shift_value, file_button, selected_steg))

        page.add(input_text, shift_value, file_button, encode_button, decode_button)

    for steg in steg_types:
        steg_button = ft.ElevatedButton(text=steg, on_click=lambda e, s=steg: on_steg_type_select(s))
        options_frame.controls.append(steg_button)

    page.add(app_label, options_frame)


# Run the Flet App
ft.app(target=main)
