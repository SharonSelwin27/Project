import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

# Import modules
import cipher
import text_steganography
import image_steganography
import video_steganography

# Configure UI appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class GraphyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GRAPHY - Steganography Tool")
        self.geometry("640x360")
        self.configure(bg="black")

        self.create_sidebar()
        self.create_splash_screen()

    def create_sidebar(self):
        """Creates a modern sidebar for navigation."""
        self.sidebar = ctk.CTkFrame(self, width=180, corner_radius=10, fg_color="black")
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="ns", padx=10, pady=10)

        # App name
        self.sidebar_label = ctk.CTkLabel(self.sidebar, text="GRAPHY", font=("Product Sans", 24, "bold"), text_color="white")
        self.sidebar_label.pack(pady=40)

        # Sidebar buttons
        self.button_text = ctk.CTkButton(self.sidebar, text="Text", command=self.show_text_ui, fg_color="black", hover_color="gray")
        self.button_text.pack(pady=10, fill="x")

        self.button_image = ctk.CTkButton(self.sidebar, text="Image", command=self.show_image_ui, fg_color="black", hover_color="gray")
        self.button_image.pack(pady=10, fill="x")

        self.button_video = ctk.CTkButton(self.sidebar, text="Video", command=self.show_video_ui, fg_color="black", hover_color="gray")
        self.button_video.pack(pady=10, fill="x")

    def create_splash_screen(self):
        """Creates the splash screen on startup."""
        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="white")
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.splash_label = ctk.CTkLabel(self.main_frame, text="GRAPHY", font=("Product Sans", 48, "bold"), text_color="black")
        self.splash_label.pack(expand=True)

    def clear_main_frame(self):
        """Clears the main frame before loading a new section."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_text_ui(self):
        """Loads the Text Steganography UI."""
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Text Steganography", font=("Product Sans", 20, "bold"), text_color="black")
        label.pack(pady=20)

        button_encode = ctk.CTkButton(self.main_frame, text="Encode", command=self.text_encode_screen, fg_color="black", hover_color="gray")
        button_encode.pack(pady=10)

        button_decode = ctk.CTkButton(self.main_frame, text="Decode", command=self.text_decode_screen, fg_color="black", hover_color="gray")
        button_decode.pack(pady=10)

    def show_image_ui(self):
        """Loads the Image Steganography UI."""
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Image Steganography", font=("Product Sans", 20, "bold"), text_color="black")
        label.pack(pady=20)

        button_encode = ctk.CTkButton(self.main_frame, text="Encode", command=self.image_encode_screen, fg_color="black", hover_color="gray")
        button_encode.pack(pady=10)

        button_decode = ctk.CTkButton(self.main_frame, text="Decode", command=self.image_decode_screen, fg_color="black", hover_color="gray")
        button_decode.pack(pady=10)

    def show_video_ui(self):
        """Loads the Video Steganography UI."""
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Video Steganography", font=("Product Sans", 20, "bold"), text_color="black")
        label.pack(pady=20)

        button_encode = ctk.CTkButton(self.main_frame, text="Encode", command=self.video_encode_screen, fg_color="black", hover_color="gray")
        button_encode.pack(pady=10)

        button_decode = ctk.CTkButton(self.main_frame, text="Decode", command=self.video_decode_screen, fg_color="black", hover_color="gray")
        button_decode.pack(pady=10)

    def text_encode_screen(self):
        """UI for encoding text steganography."""
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Encode Text", font=("Product Sans", 20))
        label.pack(pady=20)

        entry_text = ctk.CTkEntry(self.main_frame, placeholder_text="Enter text")
        entry_text.pack(pady=10)

        entry_shift = ctk.CTkEntry(self.main_frame, placeholder_text="Shift value")
        entry_shift.pack(pady=10)

        button_proceed = ctk.CTkButton(self.main_frame, text="Encrypt", command=lambda: self.encrypt_text(entry_text.get(), entry_shift.get()))
        button_proceed.pack(pady=10)

    def encrypt_text(self, text, shift):
        """Encrypts text using Caesar Cipher."""
        try:
            shift = int(shift)
            encrypted = cipher.caesar_cipher_encrypt(text, shift)
            messagebox.showinfo("Encrypted Text", encrypted)
        except ValueError:
            messagebox.showerror("Error", "Invalid shift value")

    def text_decode_screen(self):
        """UI for decoding text steganography."""
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Decode Text", font=("Product Sans", 20))
        label.pack(pady=20)

        entry_cipher = ctk.CTkEntry(self.main_frame, placeholder_text="Enter encrypted text")
        entry_cipher.pack(pady=10)

        entry_shift = ctk.CTkEntry(self.main_frame, placeholder_text="Shift value")
        entry_shift.pack(pady=10)

        button_proceed = ctk.CTkButton(self.main_frame, text="Decrypt", command=lambda: self.decrypt_text(entry_cipher.get(), entry_shift.get()))
        button_proceed.pack(pady=10)

    def decrypt_text(self, text, shift):
        """Decrypts text using Caesar Cipher."""
        try:
            shift = int(shift)
            decrypted = cipher.caesar_cipher_decrypt(text, shift)
            messagebox.showinfo("Decrypted Text", decrypted)
        except ValueError:
            messagebox.showerror("Error", "Invalid shift value")

    def image_encode_screen(self):
        """UI for encoding images."""
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Encode Image", font=("Product Sans", 20))
        label.pack(pady=20)

        button_browse = ctk.CTkButton(self.main_frame, text="Select Image", command=self.browse_image)
        button_browse.pack(pady=10)

    def browse_image(self):
        """Selects an image file."""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg")])
        if file_path:
            messagebox.showinfo("Selected", f"File: {os.path.basename(file_path)}")

    def image_decode_screen(self):
        """UI for decoding images."""
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Decode Image", font=("Product Sans", 20))
        label.pack(pady=20)

    def video_encode_screen(self):
        """UI for encoding videos."""
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Encode Video", font=("Product Sans", 20))
        label.pack(pady=20)

    def video_decode_screen(self):
        """UI for decoding videos."""
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Decode Video", font=("Product Sans", 20))
        label.pack(pady=20)


if __name__ == "__main__":
    app = GraphyApp()
    app.mainloop()
