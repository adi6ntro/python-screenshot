from datetime import datetime
from functools import partial
from PIL import Image, ImageTk
import pyscreenshot as ImageGrab
import os
import tkinter as tk

if not (os.path.isdir("snips")):
    os.mkdir("snips")

root = tk.Tk()
root.title("SWC Screenshot App")
root.iconbitmap("swc.ico")
canvas = tk.Canvas(root, width=300, height=100)
image1 = Image.open("swc.ico")
my_img1 = ImageTk.PhotoImage(image1.resize((30, 30)))

logo = tk.Label(root, image=my_img1)
canvas.create_window(150, 20, window=logo)

label = tk.Entry(root, font=('helvetica', 10),
                 bd=0, width=46)
canvas.create_window(150, 80, window=label)


def clip_screen():
    root.withdraw()
    image_name = "snips/" + \
        str(datetime.now()).replace(" ", "").replace(":", "") + ".png"
    try:
        image = ImageGrab.grab(childprocess=False)
        image.save(image_name)
        image.show()
    except Exception as e:
        print(e)
        return e
    root.deiconify()
    print("button clicked")
    return "Screenshot saved as " + image_name


def hide_window():
    root.withdraw()
    root.after(1000, get_fullscreen)


def get_fullscreen():
    label.insert(0, clip_screen())
    label.config(bd=0, state='readonly')


fs_button = tk.Button(text="Take Full Screen",
                      command=partial(hide_window),
                           bg="#8e936d", fg="black",
                           padx=10,
                           font=("Sans Serif", 9))
canvas.create_window(150, 50, window=fs_button)

canvas.pack()


if __name__ == '__main__':
    root.mainloop()
