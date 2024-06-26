import os
import sys
from PIL import Image, ImageTk

def read_image(path, size):
    if hasattr(sys, '_MEIPASS'):
        # Running in a bundle
        base_path = sys._MEIPASS
    else:
        # Running in a normal Python environment
        base_path = os.path.abspath(".")

    # Construir la ruta completa al archivo
    full_path = os.path.join(base_path, path)

    # Abrir la imagen, redimensionarla y convertirla en PhotoImage
    return ImageTk.PhotoImage(Image.open(full_path).resize(size))

def center_window(window, app_width, app_height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (app_width / 2))
    y = int((screen_height / 2) - (app_height / 2))
    return window.geometry(f"{app_width}x{app_height}+{x}+{y}")