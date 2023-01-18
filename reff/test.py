from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("SWC Screenshot App")
root.iconbitmap("swc.ico")

image = Image.open("snips/2022-12-20143504.704576.png")
my_img = ImageTk.PhotoImage(image.resize((500, 500)))
image1 = Image.open("snips/2022-12-20122109.033802.png")
my_img1 = ImageTk.PhotoImage(image1.resize((500, 500)))

image_list = [my_img, my_img1]
my_label = Label(image=image_list[0])
my_label.grid(row=0, column=0)


def showImage():
    global my_label
    my_label.grid_forget()
    # image1 = Image.open("snips/2022-12-20143504.704576.png")
    image = Image.open("snips/2022-12-20155401.155334.png")
    my_img = ImageTk.PhotoImage(image.resize((500, 500)))
    win = Toplevel()
    win.image = my_img
    my_label = Label(win, image=win.image)
    my_label.grid(row=0, column=0)
    win.focus_force()
    win.grab_set()
    win.wait_window(win)
    root.deiconify()


capture = Button(root, text="Capture Screen",
                 command=lambda: showImage()).grid(row=1, column=0)
# capture.pack()

button_quit = Button(root, text="Exit Program",
                     command=root.quit).grid(row=2, column=0)
# button_quit.pack()

root.mainloop()
