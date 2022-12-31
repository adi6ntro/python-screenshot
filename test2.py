from datetime import datetime
import tkinter as tk
from functools import partial
from tkinter import filedialog
from PIL import Image, ImageTk
import pyscreenshot as ImageGrab
import os


def onOpen():
    global photo
    filename = filedialog.askopenfilename()
    img = Image.open(filename)
    resized = img.resize((300, 300), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(resized)
    # photo = ImageTk.PhotoImage(file=filename)
    button.configure(image=photo)


def clip_screen():
    root.withdraw()
    image_name = "snips/" + \
        str(datetime.now()).replace(" ", "").replace(":", "") + ".png"
    try:
        image = ImageGrab.grab(childprocess=False)
        image.save(image_name)
    except Exception as e:
        print(e)
        return e
    root.deiconify()
    print("button clicked")
    my_path = os.path.abspath(image_name)
    # return f"{ROOT_DIR}/{image_name}"
    return f"{my_path}"


def hide_window():
    root.withdraw()
    root.after(1000, get_fullscreen)


def get_fullscreen():
    global photo
    my_path = clip_screen()
    label.insert(0, my_path)
    label.config(bd=0, state='readonly')
    img = Image.open(my_path)
    resized = img.resize((300, 300), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(resized)
    button.configure(image=photo)


root = tk.Tk()
img = Image.open("snips/2022-12-25181810.385301.png")
resized = img.resize((300, 300), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(resized)
button = tk.Button(root, image=photo, command=onOpen)
button.grid()

fs_button = tk.Button(text="Take Full Screen",
                      command=partial(hide_window),
                           bg="#8e936d", fg="black",
                           padx=10,
                           font=("Sans Serif", 9))
fs_button.grid()
label = tk.Entry(root, font=('helvetica', 10),
                 bd=0, width=30, justify='center')
label.grid()
canvas = tk.Canvas(root, width=550, height=200)
canvas.grid()


root.mainloop()
