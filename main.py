from datetime import datetime
from functools import partial
from io import BytesIO
from PIL import Image, ImageTk
import os
import time
import pyscreenshot as ImageGrab
import tkinter as tk
# import win32clipboard

if not (os.path.isdir("snips")):
    os.mkdir("snips")

root = tk.Tk()
root.title("SWC Screenshot App")
root.iconbitmap(
    "swc.png")
canvas = tk.Canvas(root, width=500, height=250, bg="lightblue")

copy_clip = tk.IntVar()
show_clip = tk.IntVar()

copy_clip_check = tk.Checkbutton(
    root, text="Copy screenshot to clipboard", variable=copy_clip)
show_clip_check = tk.Checkbutton(
    root, text="Show screenshot", variable=show_clip)

user_left = tk.Entry(root, text="")
canvas.create_window(100, 45, window=user_left)
user_top = tk.Entry(root, text="")
canvas.create_window(100, 75, window=user_top)
user_right = tk.Entry(root, text="")
canvas.create_window(100, 105, window=user_right)
user_bottom = tk.Entry(root, text="")
canvas.create_window(100, 135, window=user_bottom)

label = tk.Label(root, text="", bg="lightblue", font=('helvetica', 10))
canvas.create_window(250, 230, window=label)


# def copy_to_clipboard(filepath):
#     image = Image.open(filepath)
#     output = BytesIO()
#     image.convert("RGB").save(output, "BMP")
#     data = output.getvalue()[14:]
#     output.close()
#     send_to_clipboard(win32clipboard.CF_DIB, data)


# def send_to_clipboard(clip_type, data):
#     win32clipboard.OpenClipboard()
#     win32clipboard.EmptyClipboard()
#     win32clipboard.SetClipboardData(clip_type, data)
#     win32clipboard.CloseClipboard()


def clip_screen(dimensions):
    root.withdraw()
    # time.sleep(0.3)
    image_name = "snips/" + \
        str(datetime.now()).replace(" ", "").replace(":", "") + ".png"
    try:
        if dimensions:
            image = ImageGrab.grab(bbox=tuple(map(int, dimensions)))
        else:
            image = ImageGrab.grab()
        image.save(image_name)
        # my_img = ImageTk.PhotoImage(Image.open(image_name))
        # my_label = tk.Label(image=my_img)
        # my_label.pack()

        # if copy_clip.get():
        #     copy_to_clipboard(image_name)
        #     print("Copied to clipboard")
        # if show_clip.get():
        #     image.show()
        #     print("Show the screenshot")

    except Exception as e:
        print(e)
        return e
    root.deiconify()
    print("button clicked")
    # return "Screenshot saved as " + image_name
    return image_name


def hide_window():
    # hiding the tkinter window while taking the screenshot
    root.withdraw()
    root.after(1000, get_fullscreen)


def get_fullscreen():
    # label.configure(text=clip_screen(None))
    my_img = ImageTk.PhotoImage(Image.open(clip_screen(None)))
    label.configure(image=my_img)
    # my_label = tk.Label(image=my_img)
    # my_label.pack()


def get_dimensions():
    left = user_left.get().strip()
    top = user_top.get().strip()
    right = user_right.get().strip()
    bottom = user_bottom.get().strip()
    label.configure(text=clip_screen((left, top, right, bottom)))


dim_button = tk.Button(text="Take Dimensions",
                       command=partial(get_dimensions),
                            bg="#8e936d", fg="black",
                            padx=10,
                            font=("Sans Serif", 9))
canvas.create_window(100, 190, window=dim_button)

fs_button = tk.Button(text="Take Full Screen",
                      command=partial(hide_window),
                           bg="#8e936d", fg="black",
                           padx=10,
                           font=("Sans Serif", 9))
canvas.create_window(350, 110, window=fs_button)

# copy_clip_check.pack()
# show_clip_check.pack()
canvas.pack()
root.mainloop()
