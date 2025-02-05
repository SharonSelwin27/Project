import os
from PIL import Image
import cv2
import numpy as np

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


# --- Text Steganography ---
def encode_text_file(file_path, secret_message):
    try:
        with open(file_path, 'a') as file:
            file.write("\n" + secret_message + "###END###")  # Add delimiter
        return file_path
    except Exception as e:
        raise Exception(f"Error encoding text to file: {e}")

def decode_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        secret_message = content.split("###END###")[0]  # Extract hidden message
        return secret_message.strip()
    except Exception as e:
        raise Exception(f"Error decoding text from file: {e}")


# --- Image Steganography ---
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
                for i in range(3):  # RGB channels
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


# --- Video Steganography ---
def encode_video(video_path, secret_message):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("Error opening video file.")

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        out = cv2.VideoWriter('encoded_video.mp4', cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))
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
                        frame[y, x] = np.array(pixel, dtype=np.uint8)  # Ensure correct data type
            out.write(frame)

        cap.release()
        out.release()
        return 'encoded_video.mp4'
    except Exception as e:
        raise Exception(f"Error encoding video: {e}")

def decode_video(video_path):
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
