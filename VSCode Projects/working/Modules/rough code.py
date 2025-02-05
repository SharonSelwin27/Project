import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import cv2


# Set appearance mode to dark
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")  # Default dark color palette

# --- Caesar Cipher Functions ---
def caesar_cipher_encrypt(plaintext, shift):
    if not isinstance(shift, int):
        raise ValueError("Shift value must be an integer.")
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


# --- Text Steganography Functions ---
def encode_text_file(file_path, secret_message):
    try:
        with open(file_path, 'a') as file:
            file.write(secret_message)
        return file_path
    except Exception as e:
        raise Exception(f"Error encoding text to file: {e}")

def decode_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            secret_message = file.read()
        return secret_message
    except Exception as e:
        raise Exception(f"Error decoding text from file: {e}")


# --- Image Steganography Functions ---
def encode_image(image_path, secret_message):
    try:
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
    except Exception as e:
        raise Exception(f"Error encoding image: {e}")

def decode_image(image_path):
    try:
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
        secret_message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))

        return secret_message
    except Exception as e:
        raise Exception(f"Error decoding image: {e}")


# --- Video Steganography Functions ---
def encode_video_opencv(video_path, secret_message):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("Error opening video file.")

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
    except Exception as e:
        raise Exception(f"Error encoding video: {e}")

def decode_video_opencv(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("Error opening video file.")

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
        secret_message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))

        return secret_message
    except Exception as e:
        raise Exception(f"Error decoding video: {e}")


# --- Utility Functions ---
def get_shift_value(entry_shift):
    shift_str = entry_shift.get()
    if not shift_str.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid integer for the Caesar Cipher shift.")
        return None
    return int(shift_str)

# --- GUI Code ---
class SteganographyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Graphy")
        self.geometry("900x600")

        self.create_sidebar()
        self.create_main_frame()

    def create_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=160, height=600, corner_radius=10, bg_color="black")
        self.sidebar_frame.grid(row=0, column=0, padx=10, pady=10, rowspan=3)

        self.sidebar_label = ctk.CTkLabel(self.sidebar_frame, text="GRAPHY", font=("Product Sans", 20), text_color="white")
        self.sidebar_label.pack(pady=30)

        self.button_text = ctk.CTkButton(self.sidebar_frame, text="Text", command=self.show_text_steganography, fg_color="black", hover_color="gray")
        self.button_text.pack(pady=5, fill="x")

        self.button_image = ctk.CTkButton(self.sidebar_frame, text="Image", command=self.show_image_steganography, fg_color="black", hover_color="gray")
        self.button_image.pack(pady=5, fill="x")

        self.button_video = ctk.CTkButton(self.sidebar_frame, text="Video", command=self.show_video_steganography, fg_color="black", hover_color="gray")
        self.button_video.pack(pady=5, fill="x")

    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self, width=680, height=600, corner_radius=10, bg_color="white")
        self.main_frame.grid(row=0, column=1, padx=10, pady=10)

    def show_text_steganography(self):
        self.clear_main_frame()
        self.create_text_steganography()

    def show_image_steganography(self):
        self.clear_main_frame()
        self.create_image_steganography()

    def show_video_steganography(self):
        self.clear_main_frame()
        self.create_video_steganography()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def create_text_steganography(self):
        self.label_action = ctk.CTkLabel(self.main_frame, text="Choose Action", font=("Product Sans", 18), text_color="black")
        self.label_action.pack(padx=500,pady=20)

        self.button_encrypt = ctk.CTkButton(self.main_frame, text="Encode", command=self.text_encrypt_screen, fg_color="black", hover_color="gray")
        self.button_encrypt.pack(pady=10)

        self.button_decrypt = ctk.CTkButton(self.main_frame, text="Decode", command=self.text_decrypt_screen, fg_color="black", hover_color="gray")
        self.button_decrypt.pack(pady=10)

    def create_image_steganography(self):
        self.label_action = ctk.CTkLabel(self.main_frame, text="Choose Action", font=("Product Sans", 18), text_color="black")
        self.label_action.pack(pady=20)

        self.button_encode = ctk.CTkButton(self.main_frame, text="Encode", command=self.image_encode_screen, fg_color="black", hover_color="gray")
        self.button_encode.pack(pady=10)

        self.button_decode = ctk.CTkButton(self.main_frame, text="Decode", command=self.image_decode_screen, fg_color="black", hover_color="gray")
        self.button_decode.pack(pady=10)

    def create_video_steganography(self):
        self.label_action = ctk.CTkLabel(self.main_frame, text="Choose Action", font=("Product Sans", 18), text_color="black")
        self.label_action.pack(pady=20)

        self.button_encode = ctk.CTkButton(self.main_frame, text="Encode", command=self.video_encode_screen, fg_color="black", hover_color="gray")
        self.button_encode.pack(pady=10)

        self.button_decode = ctk.CTkButton(self.main_frame, text="Decode", command=self.video_decode_screen, fg_color="black", hover_color="gray")
        self.button_decode.pack(pady=10)

    def text_encrypt_screen(self):
        self.clear_main_frame()
        self.create_encryption_screen("Encrypt Text")

    def text_decrypt_screen(self):
        self.clear_main_frame()
        self.create_encryption_screen("Decrypt Text")

    def create_encryption_screen(self, action_type):
        self.label_action = ctk.CTkLabel(self.main_frame, text=action_type, font=("Product Sans", 16))
        self.label_action.pack(pady=20)

        self.entry_text = ctk.CTkEntry(self.main_frame, placeholder_text="Enter your text")
        self.entry_text.pack(pady=10)

        self.entry_shift = ctk.CTkEntry(self.main_frame, placeholder_text="Enter shift value")
        self.entry_shift.pack(pady=10)

        self.button_proceed = ctk.CTkButton(self.main_frame, text="Proceed", command=self.process_caesar_cipher)
        self.button_proceed.pack(pady=20)

        def browse_text(self):
        self.text_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    
    def process_caesar_cipher(self):
        shift_value = get_shift_value(self.entry_shift)
        if shift_value is None:
            return
        text = self.entry_text.get()
        action = "Encrypt" if self.label_action.cget("text") == "Encrypt Text" else "Decrypt"
        
        if action == "Encrypt":
            encrypted_text = caesar_cipher_encrypt(text, shift_value)
            messagebox.showinfo("Encrypted Text", encrypted_text)
        else:
            decrypted_text = caesar_cipher_decrypt(text, shift_value)
            messagebox.showinfo("Decrypted Text", decrypted_text)

    def image_encode_screen(self):
        self.clear_main_frame()
        self.create_image_input_screen("Encode Image")

    def image_decode_screen(self):
        self.clear_main_frame()
        self.create_image_input_screen("Decode Image")

    def create_image_input_screen(self, action_type):
        self.label_action = ctk.CTkLabel(self.main_frame, text=action_type, font=("Product Sans", 16))
        self.label_action.pack(pady=20)

        self.entry_message = ctk.CTkEntry(self.main_frame, placeholder_text="Enter secret message")
        self.entry_message.pack(pady=10)

        self.button_browse = ctk.CTkButton(self.main_frame, text="Browse Image", command=self.browse_image)
        self.button_browse.pack(pady=10)

        self.button_proceed = ctk.CTkButton(self.main_frame, text="Proceed", command=self.process_image_steganography)
        self.button_proceed.pack(pady=20)

    def browse_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    
    def process_image_steganography(self):
        secret_message = self.entry_message.get()
        if hasattr(self, 'image_path') and self.image_path:
            if self.label_action.cget("text") == "Encode Image":
                try:
                    output_path = encode_image(self.image_path, secret_message)
                    messagebox.showinfo("Success", f"Image encoded successfully: {output_path}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                try:
                    decoded_message = decode_image(self.image_path)
                    messagebox.showinfo("Decoded Message", decoded_message)
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def video_encode_screen(self):
        self.clear_main_frame()
        self.create_video_input_screen("Encode Video")

    def video_decode_screen(self):
        self.clear_main_frame()
        self.create_video_input_screen("Decode Video")

    def create_video_input_screen(self, action_type):
        self.label_action = ctk.CTkLabel(self.main_frame, text=action_type, font=("Product Sans", 16))
        self.label_action.pack(pady=20)

        self.entry_message = ctk.CTkEntry(self.main_frame, placeholder_text="Enter secret message")
        self.entry_message.pack(pady=10)

        self.button_browse = ctk.CTkButton(self.main_frame, text="Browse Video", command=self.browse_video)
        self.button_browse.pack(pady=10)

        self.button_proceed = ctk.CTkButton(self.main_frame, text="Proceed", command=self.process_video_steganography)
        self.button_proceed.pack(pady=20)

    def browse_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])

    def process_video_steganography(self):
        secret_message = self.entry_message.get()
        if hasattr(self, 'video_path') and self.video_path:
            if self.label_action.cget("text") == "Encode Video":
                try:
                    output_path = encode_video_opencv(self.video_path, secret_message)
                    messagebox.showinfo("Success", f"Video encoded successfully: {output_path}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                try:
                    decoded_message = decode_video_opencv(self.video_path)
                    messagebox.showinfo("Decoded Message", decoded_message)
                except Exception as e:
                    messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = SteganographyApp()
    app.mainloop()