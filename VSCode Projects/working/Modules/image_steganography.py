# image_steganography.py
from PIL import Image

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
