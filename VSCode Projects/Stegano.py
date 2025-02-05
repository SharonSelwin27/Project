import customtkinter as ctk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image
import string

# Caesar Cipher Encryption and Decryption Functions
def caesar_cipher(text, shift, mode='encode'):
    result = []
    
    for char in text:
        if char.isalpha():
            start = 65 if char.isupper() else 97
            offset = ord(char) - start
            shift_offset = shift if mode == 'encode' else -shift
            new_char = chr((offset + shift_offset) % 26 + start)
            result.append(new_char)
        else:
            result.append(char)
    
    return ''.join(result)

# Encode text into an image using LSB (Least Significant Bit) steganography
def encode_text_in_image(image_path, text, output_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    data = list(image.getdata())
    
    binary_text = ''.join(format(ord(c), '08b') for c in text) + '1111111111111110'  # end marker
    
    binary_data = ''.join(format(pixel[0], '08b')[:7] + format(pixel[1], '08b')[:7] + format(pixel[2], '08b')[:7] for pixel in data)
    
    if len(binary_text) > len(binary_data):
        messagebox.showerror("Error", "Text is too large to encode in this image.")
        return

    encoded_data = []
    text_index = 0
    
    for i in range(0, len(binary_data), 24):
        r, g, b = int(binary_data[i:i+8], 2), int(binary_data[i+8:i+16], 2), int(binary_data[i+16:i+24], 2)
        if text_index < len(binary_text):
            r = (r & 0xFE) | int(binary_text[text_index])
            g = (g & 0xFE) | int(binary_text[text_index+1])
            b = (b & 0xFE) | int(binary_text[text_index+2])
            text_index += 3
        encoded_data.append((r, g, b))
    
    encoded_image = Image.new('RGB', image.size)
    encoded_image.putdata(encoded_data)
    encoded_image.save(output_path)
    messagebox.showinfo("Success", "Text successfully encoded in the image.")

# Decode text from an image
def decode_text_from_image(image_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    data = list(image.getdata())
    
    binary_data = ''
    
    for pixel in data:
        binary_data += format(pixel[0], '08b')[-1] + format(pixel[1], '08b')[-1] + format(pixel[2], '08b')[-1]
    
    binary_text = ''
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        binary_text += chr(int(byte, 2))
        if binary_text[-4:] == '1110':  # End marker '1111111111111110'
            break
    
    return binary_text[:-4]

# Caesar cipher GUI and options
class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography with Caesar Cipher")
        self.root.geometry("600x400")
        
        # Labels and Buttons for the UI
        self.shift_label = ctk.CTkLabel(root, text="Enter Caesar Shift Value:")
        self.shift_label.pack(pady=10)
        
        self.shift_entry = ctk.CTkEntry(root)
        self.shift_entry.pack(pady=5)
        
        self.encode_button = ctk.CTkButton(root, text="Encode Text/Image/Video", command=self.encode_file)
        self.encode_button.pack(pady=10)
        
        self.decode_button = ctk.CTkButton(root, text="Decode Image/Video", command=self.decode_file)
        self.decode_button.pack(pady=10)
        
    def encode_file(self):
        shift = int(self.shift_entry.get())
        text = filedialog.askopenfilename(title="Select Text File", filetypes=(("Text files", "*.txt"),))
        if text:
            with open(text, 'r') as file:
                plaintext = file.read()
            cipher_text = caesar_cipher(plaintext, shift, mode='encode')
            
            file_type = filedialog.askopenfilename(title="Select Image or Video", filetypes=(("Image Files", "*.png;*.jpg;*.jpeg"), ("Video Files", "*.mp4;*.avi;*.mov")))
            
            if file_type:
                if file_type.endswith(('png', 'jpg', 'jpeg')):
                    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
                    encode_text_in_image(file_type, cipher_text, output_path)
                else:
                    messagebox.showinfo("Info", "Video encoding not supported in this version.")
                
    def decode_file(self):
        file_type = filedialog.askopenfilename(title="Select Image or Video", filetypes=(("Image Files", "*.png;*.jpg;*.jpeg"), ("Video Files", "*.mp4;*.avi;*.mov")))
        
        if file_type:
            if file_type.endswith(('png', 'jpg', 'jpeg')):
                decoded_text = decode_text_from_image(file_type)
                messagebox.showinfo("Decoded Text", decoded_text)
            else:
                messagebox.showinfo("Info", "Video decoding not supported in this version.")

# Initialize GUI
if __name__ == "__main__":
    root = ctk.CTk()
    app = SteganographyApp(root)
    root.mainloop()
