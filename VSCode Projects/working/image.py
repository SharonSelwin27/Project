import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import cv2

# ----------------- Application Configuration -----------------
ctk.set_appearance_mode("dark")  # Set dark mode
root = ctk.CTk()
root.title("GRAPHY")
root.geometry("1024x768")
root.configure(bg="#1e1e1e")

# Global variables
main_content = ctk.CTkFrame(root)  # Main content area
main_content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

entry_message = None
entry_shift = None
encoded_image = None

# ----------------- Helper Functions -----------------
def clear_main_content():
    """Clears all widgets from the main content frame."""
    for widget in main_content.winfo_children():
        widget.destroy()

def get_shift_value():
    """Gets a valid integer shift value for Caesar Cipher."""
    shift_str = entry_shift.get()
    if not shift_str.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid integer for the Caesar Cipher shift.")
        return None
    return int(shift_str)

# ----------------- Caesar Cipher Encryption & Decryption -----------------
def caesar_cipher_encrypt(plaintext, shift):
    """Encrypts a message using Caesar Cipher."""
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
    """Decrypts a message using Caesar Cipher."""
    return caesar_cipher_encrypt(ciphertext, -shift)

# ----------------- Image Steganography -----------------
def image_steganography_screen():
    """Displays Image Steganography selection screen."""
    clear_main_content()

    ctk.CTkLabel(main_content, text="Image Steganography", font=("Arial", 30, "bold"), text_color="#FFFFFF").pack(pady=(50, 20))

    ctk.CTkButton(main_content, text="Encode", width=350, height=50, fg_color="#28a745", hover_color="#218838",
                  text_color="#ffffff", corner_radius=10, command=image_encode_screen).pack(pady=10)
    
    ctk.CTkButton(main_content, text="Decode", width=350, height=50, fg_color="#dc3545", hover_color="#c82333",
                  text_color="#ffffff", corner_radius=10, command=image_decode_screen).pack(pady=10)

# ----------------- Encoding Screen -----------------
def image_encode_screen():
    """Displays the screen for encoding text in an image."""
    global entry_message, entry_shift
    clear_main_content()

    ctk.CTkLabel(main_content, text="Encode Text in Image", font=("Arial", 30, "bold"), text_color="#FFFFFF").pack(pady=(30, 20))

    entry_message = ctk.CTkTextbox(main_content, height=100, width=400, fg_color="#333333", text_color="#ffffff", corner_radius=10)
    entry_message.pack(pady=10)

    entry_shift = ctk.CTkEntry(main_content, placeholder_text="Enter shift for Caesar Cipher", width=400, fg_color="#333333", text_color="#ffffff", corner_radius=10)
    entry_shift.pack(pady=10)

    ctk.CTkButton(main_content, text="Select Image", width=350, height=40, fg_color="#007bff", hover_color="#0056b3",
                  text_color="#ffffff", corner_radius=10, command=select_image_to_encode).pack(pady=10)

# ----------------- Decoding Screen -----------------
def image_decode_screen():
    """Displays the screen for decoding text from an image."""
    global entry_shift
    clear_main_content()

    ctk.CTkLabel(main_content, text="Decode Text from Image", font=("Arial", 30, "bold"), text_color="#FFFFFF").pack(pady=(30, 20))

    entry_shift = ctk.CTkEntry(main_content, placeholder_text="Enter shift for Caesar Cipher", width=400, fg_color="#333333", text_color="#ffffff", corner_radius=10)
    entry_shift.pack(pady=10)

    ctk.CTkButton(main_content, text="Select Image", width=350, height=40, fg_color="#ff8800", hover_color="#cc7000",
                  text_color="#ffffff", corner_radius=10, command=select_image_to_decode).pack(pady=10)

# ----------------- Encoding and Decoding Functions -----------------
def select_image_to_encode():
    """Selects an image and encodes a message in it."""
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not image_path:
        return

    image = cv2.imread(image_path)
    secret_message = entry_message.get("1.0", "end-1c").strip()
    if not secret_message:
        messagebox.showerror("Input Error", "Please enter a message to encode.")
        return

    shift = get_shift_value()
    if shift is None:
        return

    encrypted_message = caesar_cipher_encrypt(secret_message, shift)
    encoded_image = encode_text_in_image(image, encrypted_message)

    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if save_path:
        cv2.imwrite(save_path, encoded_image)
        messagebox.showinfo("Encoding Complete", f"Image with encoded text saved as {save_path}")

def select_image_to_decode():
    """Selects an image and decodes the hidden message from it."""
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not image_path:
        return

    image = cv2.imread(image_path)
    decoded_message = decode_text_from_image(image)

    if decoded_message:
        shift = get_shift_value()
        if shift is None:
            return

        decrypted_message = caesar_cipher_decrypt(decoded_message, shift)

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if save_path:
            with open(save_path, 'w') as output_file:
                output_file.write(decrypted_message)
            messagebox.showinfo("Decoding Complete", f"Decrypted text saved as {save_path}")
    else:
        messagebox.showerror("Decoding Error", "No hidden message found in the image.")

def encode_text_in_image(image, message):
    """Encodes the given message in the image."""
    binary_message = ''.join(format(ord(char), '08b') for char in message)  # Convert message to binary
    message_len = len(binary_message)
    image_data = np.array(image)
    pixel_index = 0

    for i in range(image_data.shape[0]):
        for j in range(image_data.shape[1]):
            for c in range(3):  # Iterate through R, G, B channels
                if pixel_index < message_len:
                    image_data[i, j][c] = (image_data[i, j][c] & 0xFE) | int(binary_message[pixel_index])
                    pixel_index += 1
                if pixel_index >= message_len:
                    break

    return image_data

def decode_text_from_image(image):
    """Decodes the hidden message from the image."""
    image_data = np.array(image)
    binary_message = ""
    for i in range(image_data.shape[0]):
        for j in range(image_data.shape[1]):
            for c in range(3):  # Iterate through R, G, B channels
                binary_message += str(image_data[i, j][c] & 1)

    # Split binary message into 8-bit chunks and convert to characters
    byte_size = 8
    message = ""
    for i in range(0, len(binary_message), byte_size):
        byte = binary_message[i:i + byte_size]
        if len(byte) == byte_size:
            message += chr(int(byte, 2))

    return message.rstrip('\x00')  # Remove padding

# ----------------- UI Navigation -----------------
def show_screen(screen_type):
    """Handles navigation between different steganography screens."""
    clear_main_content()
    if screen_type == "Text":
        text_steganography_screen()
    elif screen_type == "Image":
        image_steganography_screen()
    elif screen_type == "Video":
        video_steganography_screen()

# ----------------- Sidebar Navigation -----------------
def create_sidebar():
    """Creates the navigation sidebar."""
    sidebar = ctk.CTkFrame(root, width=250, height=768, fg_color="#212121", corner_radius=15)
    sidebar.pack(side="left", fill="y", padx=10, pady=10)

    ctk.CTkLabel(sidebar, text="GRAPHY", font=("Arial", 24, "bold"), text_color="#FFFFFF").pack(pady=(20, 30))

    ctk.CTkButton(sidebar, text="Text", width=220, height=45, fg_color="#333333", hover_color="#444444",
                  text_color="#ffffff", corner_radius=20, command=lambda: show_screen("Text")).pack(pady=10)

    ctk.CTkButton(sidebar, text="Image", width=220, height=45, fg_color="#333333", hover_color="#444444",
                  text_color="#ffffff", corner_radius=20, command=lambda: show_screen("Image")).pack(pady=10)

    ctk.CTkButton(sidebar, text="Quit", width=220, height=45, fg_color="#333333", hover_color="#444444",
                  text_color="#ffffff", corner_radius=20, command=root.quit).pack(pady=10)

# Initialize Sidebar
create_sidebar()

# Start the UI
root.mainloop()
