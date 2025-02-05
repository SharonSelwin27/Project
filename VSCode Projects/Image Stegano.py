# image_steganography.py

from PIL import Image

def encode_image(image_path, secret_message, output_image_path):
    image = Image.open(image_path)
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message) + '1111111111111110'  # End delimiter
    
    if len(binary_message) > image.width * image.height * 3:
        raise ValueError("Message is too large to hide in this image.")
    
    pixels = image.load()
    binary_index = 0
    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            if binary_index < len(binary_message):
                # Modify the least significant bit of each color channel
                r = (r & 0xFE) | int(binary_message[binary_index])
                binary_index += 1
            if binary_index < len(binary_message):
                g = (g & 0xFE) | int(binary_message[binary_index])
                binary_index += 1
            if binary_index < len(binary_message):
                b = (b & 0xFE) | int(binary_message[binary_index])
                binary_index += 1
            pixels[x, y] = (r, g, b)
    
    image.save(output_image_path)

def decode_image(image_path):
    image = Image.open(image_path)
    pixels = image.load()
    binary_message = ''
    
    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            binary_message += str(r & 1)
            binary_message += str(g & 1)
            binary_message += str(b & 1)
    
    # Split the binary message into chunks of 8 to convert it back to characters
    byte_array = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    decoded_message = ''.join(chr(int(byte, 2)) for byte in byte_array)
    
    # Find the end delimiter (the "1111111111111110" binary sequence) and return the message
    return decoded_message.split('1111111111111110')[0]
