from datetime import datetime
from functools import partial
from PIL import Image, ImageTk
from sys import platform
from tkinter import Tk, filedialog, Frame, Button, Canvas, Label, Entry
import pyscreenshot as ImageGrab
import os


class Gui():
    def __init__(self, master):
        self.master = master
        self.num_list = []
        self.num = 0
        self.x = self.y = 0
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.screenshot_widgets()
        self.create_widgets()
        # Button(self.master, text="Add Box Shape", command=self.on_click).pack()
        Button(self.master, text="Delete Image",
               command=self.delete_image).pack()
        Button(self.master, text="Delete Box",
               command=self.delete_box).pack()

    def screenshot_widgets(self):
        self.canvas_top = Canvas(self.master, width=300, height=100)
        image1 = Image.open("swc.ico")
        my_img1 = ImageTk.PhotoImage(image1.resize((30, 30)))

        self.logo = Label(self.master, image=my_img1)
        self.canvas_top.create_window(150, 20, window=self.logo)

        self.label = Entry(self.master, font=('helvetica', 10),
                           bd=0, width=30, justify='center')
        self.canvas_top.create_window(150, 80, window=self.label)

        fs_button = Button(text="Take Full Screen",
                           command=partial(self.hide_window),
                                bg="#8e936d", fg="black",
                                padx=10,
                                font=("Sans Serif", 9))
        self.canvas_top.create_window(150, 50, window=fs_button)

        self.canvas_top.pack()

    def create_widgets(self):
        self.select = Button(
            self.master, text="select an image", command=self.select_image)
        self.select.pack()
        self.canvas = Canvas(self.master, width=400,
                             height=400, bg="grey", cursor="cross")

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Configure>", lambda e: self.canvas.config(
            scrollregion=self.canvas.bbox("all")))

        self.canvas.pack()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        # create rectangle if not yet exist
        if not self.rect:
            self.rect = self.canvas.create_rectangle(
                self.x, self.y, 1, 1, outline='red', width=3)
            self.num_list.insert(0, self.rect)

    def on_move_press(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)

        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if event.x > 0.9*w:
            self.canvas.xview_scroll(1, 'units')
        elif event.x < 0.1*w:
            self.canvas.xview_scroll(-1, 'units')
        if event.y > 0.9*h:
            self.canvas.yview_scroll(1, 'units')
        elif event.y < 0.1*h:
            self.canvas.yview_scroll(-1, 'units')

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)
        coordinates = self.start_x, self.start_y, curX, curY
        # print(coordinates)
        cek = self.canvas.create_rectangle(
            coordinates, outline='red', width=3)
        self.num_list.insert(0, cek)

    def select_image(self):
        self.canvas.delete(self.num)
        file_path = filedialog.askopenfilename()
        des = Image.open(file_path)
        bg_image = ImageTk.PhotoImage(des)
        self.canvas.bg_image = bg_image
        cek = self.canvas.create_image(
            0, 0, anchor="nw", image=self.canvas.bg_image)

        self.num = cek

    def on_click(self):
        coordinates = 50, 0, 100, 50
        self.canvas.create_rectangle(
            coordinates, outline='red', width=3)
        # self.num += 1
        # self.num_list.insert(0, self.num)

    def delete_box(self):
        # self.canvas.delete("all")
        if len(self.num_list) > 0:
            self.canvas.delete(self.num_list[0])
            self.num_list.pop(0)

    def delete_image(self):
        if self.num > 0:
            self.canvas.delete(self.num)
            self.num = 0

    def clip_screen(self):
        # self.master.withdraw()
        image_name = "snips/" + \
            str(datetime.now()).replace(" ", "").replace(":", "") + ".png"
        try:
            image = ImageGrab.grab(childprocess=False)
            image.save(image_name)
            img = Image.open(image_name)
            resized = img.resize((30, 30), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(resized)
            self.logo.configure(image=photo)
            self.canvas_top.create_window(150, 20, window=self.logo)

        except Exception as e:
            print(e)
            return e
        self.master.deiconify()
        print("button clicked")
        my_path = os.path.abspath(image_name)
        return f"{my_path}"

    def hide_window(self):
        self.master.withdraw()
        self.master.after(1000, self.get_fullscreen)

    def get_fullscreen(self):
        my_path = self.clip_screen()
        self.label.insert(0, my_path)
        self.label.config(bd=0, state='readonly')
        if platform == "win32":
            os.system(my_path)


if __name__ == "__main__":
    if not (os.path.isdir("snips")):
        os.mkdir("snips")
    root = Tk()
    root.title("SWC Screenshot App")
    root.iconbitmap("swc.ico")
    root.resizable(0, 0)
    my_gui = Gui(root)
    root.mainloop()
