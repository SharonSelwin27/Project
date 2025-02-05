# video_steganography.py
import cv2

def encode_video_opencv(video_path, secret_message):
    cap = cv2.VideoCapture(video_path)
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

def decode_video_opencv(video_path):
    cap = cv2.VideoCapture(video_path)
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
    secret_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    
    return secret_message
