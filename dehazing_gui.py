import cv2
import numpy as np
from tkinter import Tk, Button, Label
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

# ----------------------------
# Basic Dehazing Function using CLAHE
# ----------------------------
def dehaze_image(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)

    limg = cv2.merge((cl, a, b))
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return final

# ----------------------------
# GUI Functions
# ----------------------------
def upload_image():
    file_path = askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        dehazed_image = dehaze_image(image)

        # Convert to RGB for PIL
        rgb_image = cv2.cvtColor(dehazed_image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_image)
        tk_image = ImageTk.PhotoImage(pil_image)

        label.config(image=tk_image)
        label.image = tk_image  # Keep a reference

# ----------------------------
# GUI Setup
# ----------------------------
root = Tk()
root.title("Image Dehazing GUI")

label = Label(root)
label.pack()

button = Button(root, text="Upload and Dehaze Image", command=upload_image)
button.pack()

root.mainloop()
