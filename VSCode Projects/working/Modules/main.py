# main.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
from caesar_cipher import caesar_cipher_encrypt, caesar_cipher_decrypt
from image_steganography import encode_image, decode_image
from video_steganography import encode_video_opencv, decode_video_opencv
from text_steganography import encode_text_file, decode_text_file
from utils import get_shift_value

ctk.set_appearance_mode("dark")
