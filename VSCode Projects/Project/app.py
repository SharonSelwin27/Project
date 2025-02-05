from flask import Flask, request, jsonify
import os
from PIL import Image
import cv2
import numpy as np
from io import BytesIO

app = Flask(__name__)

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

# --- Steganography Functions ---
def encode_text_file(file_path, secret_message):
    with open(file_path, 'a') as file:
        file.write("\n" + secret_message + "###END###")
    return file_path

def decode_text_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    secret_message = content.split("###END###")[0]
    return secret_message.strip()

def encode_image(image, secret_message):
    binary_message = ''.join(format(ord(i), '08b') for i in secret_message) + '1111111111111110'
    image = Image.open(image)
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

def decode_image(image):
    image = Image.open(image)
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

def encode_video(video, secret_message):
    cap = cv2.VideoCapture(video)
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
                    frame[y, x] = np.array(pixel, dtype=np.uint8)
        out.write(frame)
    cap.release()
    out.release()
    return 'encoded_video.mp4'

def decode_video(video):
    cap = cv2.VideoCapture(video)
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

@app.route('/encode-text', methods=['POST'])
def encode_text():
    data = request.json
    secret_message = data['message']
    file_path = 'encoded_text.txt'
    encode_text_file(file_path, secret_message)
    return jsonify({'message': 'Text encoded successfully', 'file': file_path})

@app.route('/decode-text', methods=['POST'])
def decode_text():
    data = request.json
    file_path = data['file']
    secret_message = decode_text_file(file_path)
    return jsonify({'message': 'Text decoded successfully', 'secret': secret_message})

@app.route('/encode-image', methods=['POST'])
def encode_image_route():
    file = request.files['image']
    secret_message = request.form['message']
    encoded_image = encode_image(file, secret_message)
    return jsonify({'message': 'Image encoded successfully', 'file': encoded_image})

@app.route('/decode-image', methods=['POST'])
def decode_image_route():
    file = request.files['image']
    secret_message = decode_image(file)
    return jsonify({'message': 'Image decoded successfully', 'secret': secret_message})

@app.route('/encode-video', methods=['POST'])
def encode_video_route():
    file = request.files['video']
    secret_message = request.form['message']
    encoded_video = encode_video(file, secret_message)
    return jsonify({'message': 'Video encoded successfully', 'file': encoded_video})

@app.route('/decode-video', methods=['POST'])
def decode_video_route():
    file = request.files['video']
    secret_message = decode_video(file)
    return jsonify({'message': 'Video decoded successfully', 'secret': secret_message})

if __name__ == '__main__':
    app.run(debug=True)
