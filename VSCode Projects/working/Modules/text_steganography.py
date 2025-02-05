# text_steganography.py

def encode_text_file(file_path, secret_message):
    with open(file_path, 'a') as file:
        file.write(secret_message)
    return file_path

def decode_text_file(file_path):
    with open(file_path, 'r') as file:
        secret_message = file.read()
    return secret_message
