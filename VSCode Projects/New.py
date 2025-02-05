# text_steganography.py

def encode_message(original_text, secret_message):
    # Encode secret message as binary
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
    # Ensure the original text is long enough
    if len(binary_message) > len(original_text):
        raise ValueError("Secret message is too long to hide in the given text.")
    
    encoded_text = list(original_text)
    binary_index = 0
    
    # Embed the binary message in the least significant bit of each character's ASCII value
    for i in range(len(encoded_text)):
        if binary_index < len(binary_message):
            encoded_text[i] = chr(ord(encoded_text[i]) & 0xFE | int(binary_message[binary_index]))
            binary_index += 1
    return ''.join(encoded_text)

def decode_message(encoded_text):
    # Extract the binary message from the least significant bit of each character's ASCII value
    binary_message = ''
    for char in encoded_text:
        binary_message += str(ord(char) & 1)
    
    # Split the binary message into chunks of 8 to convert it back to characters
    byte_array = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    decoded_message = ''.join(chr(int(byte, 2)) for byte in byte_array)
    return decoded_message.rstrip('\x00')  # Remove padding
