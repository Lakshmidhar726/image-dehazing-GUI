import cv2
import numpy as np
from tkinter import Tk, Button, Label
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
def white_balance(img):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] -= ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] -= ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    return cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
def enhance_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    merged = cv2.merge((cl, a, b))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
def fuse_images(img1, img2):
    return cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
def open_image():
    file_path = askopenfilename()
    if not file_path:
        return

    img = cv2.imread(file_path)
    img = cv2.resize(img, (500, 400))

    first_input = white_balance(img)
    second_input = enhance_contrast(img)
    dehazed = fuse_images(first_input, second_input)

    display_images(img, first_input, second_input, dehazed)
def display_images(original, input1, input2, output):
    for widget in window.winfo_children():
        widget.destroy()

    images = [original, input1, input2, output]
    titles = ['Original', 'White Balanced', 'Contrast Enhanced', 'Dehazed']

    for i in range(4):
        bgr_img = cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(bgr_img)
        img_tk = ImageTk.PhotoImage(img_pil)

        label = Label(window, image=img_tk, text=titles[i], compound='top', font=('Arial', 12))
        label.image = img_tk
        label.grid(row=0, column=i, padx=5, pady=5)

    Button(window, text='Open Image', command=open_image).grid(row=1, column=1, columnspan=2, pady=20)
window = Tk()
window.title("Image Dehazing GUI")
window.geometry("2100x600")
Button(window, text='Open Image', command=open_image).pack(pady=20)
window.mainloop()
