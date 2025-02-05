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

# ----------------- Text Steganography -----------------
def text_steganography_screen():
    """Displays Text Steganography selection screen."""
    clear_main_content()

    ctk.CTkLabel(main_content, text="Text Steganography", font=("Arial", 30, "bold"), text_color="#FFFFFF").pack(pady=(50, 20))

    ctk.CTkButton(main_content, text="Encode", width=350, height=50, fg_color="#28a745", hover_color="#218838",
                  text_color="#ffffff", corner_radius=10, command=text_encode_screen).pack(pady=10)
    
    ctk.CTkButton(main_content, text="Decode", width=350, height=50, fg_color="#dc3545", hover_color="#c82333",
                  text_color="#ffffff", corner_radius=10, command=text_decode_screen).pack(pady=10)

# ----------------- Encoding Screen -----------------
def text_encode_screen():
    """Displays the screen for encoding text with Caesar Cipher."""
    global entry_message, entry_shift
    clear_main_content()

    ctk.CTkLabel(main_content, text="Encode Text", font=("Arial", 30, "bold"), text_color="#FFFFFF").pack(pady=(30, 20))

    entry_message = ctk.CTkTextbox(main_content, height=100, width=400, fg_color="#333333", text_color="#ffffff", corner_radius=10)
    entry_message.pack(pady=10)

    entry_shift = ctk.CTkEntry(main_content, placeholder_text="Enter shift for Caesar Cipher", width=400, fg_color="#333333", text_color="#ffffff", corner_radius=10)
    entry_shift.pack(pady=10)

    ctk.CTkButton(main_content, text="Save to File", width=350, height=40, fg_color="#007bff", hover_color="#0056b3",
                  text_color="#ffffff", corner_radius=10, command=save_encoded_text).pack(pady=10)

# ----------------- Decoding Screen -----------------
def text_decode_screen():
    """Displays the screen for decoding text with Caesar Cipher."""
    global entry_shift
    clear_main_content()

    ctk.CTkLabel(main_content, text="Decode Text", font=("Arial", 30, "bold"), text_color="#FFFFFF").pack(pady=(30, 20))

    entry_shift = ctk.CTkEntry(main_content, placeholder_text="Enter shift for Caesar Cipher", width=400, fg_color="#333333", text_color="#ffffff", corner_radius=10)
    entry_shift.pack(pady=10)

    ctk.CTkButton(main_content, text="Select File", width=350, height=40, fg_color="#ff8800", hover_color="#cc7000",
                  text_color="#ffffff", corner_radius=10, command=open_file_to_decode_text).pack(pady=10)

# ----------------- Encoding and Decoding Functions -----------------
def save_encoded_text():
    """Encrypts and saves the text to a file."""
    shift = get_shift_value()
    if shift is None:
        return

    secret_message = entry_message.get("1.0", "end-1c").strip()
    if not secret_message:
        messagebox.showerror("Input Error", "Please enter a message to encode.")
        return

    encrypted_message = caesar_cipher_encrypt(secret_message, shift)

    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if save_path:
        with open(save_path, 'w') as output_file:
            output_file.write(encrypted_message)
        messagebox.showinfo("Encoding Complete", f"Encrypted text saved as {save_path}")

def open_file_to_decode_text():
    """Opens an encrypted file and deciphers the message."""
    file_path = filedialog.askopenfilename(title="Select Text File to Decode", filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return

    with open(file_path, 'r') as file:
        secret_message = file.read()

    shift = get_shift_value()
    if shift is None:
        return

    decrypted_message = caesar_cipher_decrypt(secret_message, shift)

    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if save_path:
        with open(save_path, 'w') as output_file:
            output_file.write(decrypted_message)
        messagebox.showinfo("Decoding Complete", f"Decrypted text saved as {save_path}")

# ----------------- Sidebar Navigation -----------------
def create_sidebar():
    """Creates the navigation sidebar."""
    sidebar = ctk.CTkFrame(root, width=250, height=768, fg_color="#212121", corner_radius=15)
    sidebar.pack(side="left", fill="y", padx=10, pady=10)

    ctk.CTkLabel(sidebar, text="GRAPHY", font=("Arial", 24, "bold"), text_color="#FFFFFF").pack(pady=(20, 30))

    ctk.CTkButton(sidebar, text="Text", width=220, height=45, fg_color="#333333", hover_color="#444444",
                  text_color="#ffffff", corner_radius=20, command=lambda: show_screen("Text")).pack(pady=10)

    ctk.CTkButton(sidebar, text="Quit", width=220, height=45, fg_color="#333333", hover_color="#444444",
                  text_color="#ffffff", corner_radius=20, command=root.quit).pack(pady=10)

# Initialize Sidebar
create_sidebar()

# Start the UI
root.mainloop()