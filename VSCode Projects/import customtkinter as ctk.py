import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import cv2

# Set appearance mode
ctk.set_appearance_mode("dark")

# Initialize the main window
root = ctk.CTk()
root.title("GRAPHY")
root.geometry("1024x768")
root.configure(bg="#1e1e1e")

# Global variable to store the main content frame
main_content = ctk.CTkFrame(root)
main_content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Global variables for text input fields
entry_message = None
entry_shift = None

# Caesar Cipher Encryption and Decryption Functions
def caesar_cipher_encrypt(plaintext, shift):
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

# Function to clear the main content area
def clear_main_content():
    global main_content
    for widget in main_content.winfo_children():
        widget.destroy()

# Function to display the selected screen
def show_screen(screen_type):
    clear_main_content()
    if screen_type == "Text":
        go_to_text_steganography()
    elif screen_type == "Image":
        go_to_image_steganography()
    elif screen_type == "Video":
        go_to_video_steganography()

# Function for Text Steganography Selection Screen
def go_to_text_steganography():
    clear_main_content()
    
    label = ctk.CTkLabel(main_content, text="Text Steganography", font=("Arial", 30, "bold"), text_color="#FFFFFF")
    label.pack(pady=(50, 20))

    encode_btn = ctk.CTkButton(main_content, text="Encode", width=350, height=50, fg_color="#28a745", hover_color="#218838", text_color="#ffffff", corner_radius=10, command=go_to_encode_screen)
    encode_btn.pack(pady=10)

    decode_btn = ctk.CTkButton(main_content, text="Decode", width=350, height=50, fg_color="#dc3545", hover_color="#c82333", text_color="#ffffff", corner_radius=10, command=go_to_decode_screen)
    decode_btn.pack(pady=10)

# Function for Encoding Screen
def go_to_encode_screen():
    global entry_message, entry_shift
    clear_main_content()

    label = ctk.CTkLabel(main_content, text="Encode Text", font=("Arial", 30, "bold"), text_color="#FFFFFF")
    label.pack(pady=(30, 20))

    entry_message = ctk.CTkTextbox(main_content, height=100, width=400, fg_color="#333333", text_color="#ffffff", corner_radius=10)
    entry_message.pack(pady=10)

    entry_shift = ctk.CTkEntry(main_content, placeholder_text="Enter shift for Caesar Cipher", width=400, fg_color="#333333", text_color="#ffffff", corner_radius=10)
    entry_shift.pack(pady=10)

    save_btn = ctk.CTkButton(main_content, text="Save to File", width=350, height=40, fg_color="#007bff", hover_color="#0056b3", text_color="#ffffff", corner_radius=10, command=save_encoded_text)
    save_btn.pack(pady=10)

# Function for Decoding Screen
def go_to_decode_screen():
    global entry_shift
    clear_main_content()

    label = ctk.CTkLabel(main_content, text="Decode Text", font=("Arial", 30, "bold"), text_color="#FFFFFF")
    label.pack(pady=(30, 20))

    entry_shift = ctk.CTkEntry(main_content, placeholder_text="Enter shift for Caesar Cipher", width=400, fg_color="#333333", text_color="#ffffff", corner_radius=10)
    entry_shift.pack(pady=10)

    select_btn = ctk.CTkButton(main_content, text="Select File", width=350, height=40, fg_color="#ff8800", hover_color="#cc7000", text_color="#ffffff", corner_radius=10, command=open_file_to_decode_text)
    select_btn.pack(pady=10)

# Function to get a valid Caesar Cipher shift value
def get_shift_value():
    shift_str = entry_shift.get()
    if not shift_str.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid integer for the Caesar Cipher shift.")
        return None
    return int(shift_str)

# Function to save encoded text to file
def save_encoded_text():
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

# Function to open file and decode text
def open_file_to_decode_text():
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

# Sidebar navigation
def create_sidebar():
    sidebar = ctk.CTkFrame(root, width=250, height=768, fg_color="#212121", corner_radius=15)
    sidebar.pack(side="left", fill="y", padx=10, pady=10)

    label = ctk.CTkLabel(sidebar, text="GRAPHY", font=("Arial", 24, "bold"), text_color="#FFFFFF")
    label.pack(pady=(20, 30))

    btn_text = ctk.CTkButton(sidebar, text="Text", width=220, height=45, fg_color="#333333", hover_color="#444444", text_color="#ffffff", corner_radius=20, command=lambda: show_screen("Text"))
    btn_text.pack(pady=10)

    btn_image = ctk.CTkButton(sidebar, text="Image", width=220, height=45, fg_color="#333333", hover_color="#444444", text_color="#ffffff", corner_radius=20, command=lambda: show_screen("Image"))
    btn_image.pack(pady=10)

    btn_video = ctk.CTkButton(sidebar, text="Video", width=220, height=45, fg_color="#333333", hover_color="#444444", text_color="#ffffff", corner_radius=20, command=lambda: show_screen("Video"))
    btn_video.pack(pady=10)

    btn_quit = ctk.CTkButton(sidebar, text="Quit", width=220, height=45, fg_color="#333333", hover_color="#444444", text_color="#ffffff", corner_radius=20, command=root.quit)
    btn_quit.pack(pady=10)

# Initialize Sidebar
create_sidebar()

# Start the UI
root.mainloop()
