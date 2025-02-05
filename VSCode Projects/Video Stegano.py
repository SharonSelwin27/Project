# video_steganography.py

import cv2
import numpy as np

def encode_video(video_path, secret_message, output_video_path):
    # Open video
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    width = int(cap.get(3))
    height = int(cap.get(4))
    out = cv2.VideoWriter(output_video_path, fourcc, 30.0, (width, height))
    
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message) + '1111111111111110'  # End delimiter
    frame_index = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the frame to a numpy array and flatten it for manipulation
        frame = np.array(frame)
        frame_shape = frame.shape
        flat_frame = frame.flatten()
        
        for i in range(len(binary_message)):
            flat_frame[i] = (flat_frame[i] & 0xFE) | int(binary_message[i])  # Alter LSB of pixel values
        
        # Reshape the flattened array back to the original frame shape
        encoded_frame = flat_frame.reshape(frame_shape)
        
        # Write the frame with the hidden message
        out.write(encoded_frame)
        frame_index += 1
    
    cap.release()
    out.release()

def decode_video(video_path):
    # Open video
    cap = cv2.VideoCapture(video_path)
    binary_message = ''
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the frame to a numpy array and flatten it for manipulation
        frame = np.array(frame)
        flat_frame = frame.flatten()
        
        for i in range(len(flat_frame)):
            binary_message += str(flat_frame[i] & 1)  # Get the least significant bit
        
    cap.release()
    
    # Split the binary message into chunks of 8 to convert it back to characters
    byte_array = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    decoded_message = ''.join(chr(int(byte, 2)) for byte in byte_array)
    
    # Find the end delimiter (the "1111111111111110" binary sequence) and return the message
    return decoded_message.split('1111111111111110')[0]
