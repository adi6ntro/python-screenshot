from datetime import datetime
from functools import partial
from PIL import Image, ImageTk
from sys import platform
from tkinter import Tk, filedialog, Frame, Button, Canvas, Label, Entry, LabelFrame, Scrollbar, Text, StringVar, OptionMenu, E, W
import pyscreenshot as ImageGrab
import os


class Gui():
    def __init__(self, master):
        self.master = master
        self.num_list = []
        self.box_delete = {}
        self.cat = {"Not Exposed": 0, "Exposed": 0,
                    "Periapical": 0, "Bone Loss": 0, "RCT": 0}
        self.num = 0
        self.x = self.y = 0
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.outline = "#%02x%02x%02x" % (255, 0, 0)
        self.screenshot_widgets()
        self.create_canvas()
        # Button(self.master, text="Add Box Shape", command=self.on_click).grid()
        # Button(self.master, text="Box - Not Exposed",
        #        command=lambda: self.outline_color('Not_Exposed_')).grid()
        # Button(self.master, text="Box - Exposed",
        #        command=lambda: self.outline_color('Exposed_')).grid()
        # Button(self.master, text="Box - Periapical",
        #        command=lambda: self.outline_color('Periapical_')).grid()
        # Button(self.master, text="Box - Bone_Loss",
        #        command=lambda: self.outline_color('Bone_Loss')).grid()
        # Button(self.master, text="Box - RCT",
        #        command=lambda: self.outline_color('RCT')).grid()
        Button(self.master, text="Delete Image",
               command=self.delete_image).grid()
        self.create_categories()
        self.create_box_list()
        # Button(self.master, text="Delete Box",
        #        command=self.delete_box).grid()
        # Button(self.master, text="Get Box",
        #        command=self.get_box).grid()

    # def get_box(self):
    #     for r in self.num_list:
    #         Button(self.master, text="Box " + str(r),
    #                command=self.delete_box).grid()

    # def outline_color(self, color_type):
    #     print(color_type)
    #     if color_type == "Not_Exposed_":
    #         color = (255, 0, 0)
    #     elif color_type == "Exposed_":
    #         color = (0, 0, 255)
    #     elif color_type == "Periapical_":
    #         color = (0, 255, 0)
    #     elif color_type == "Bone_Loss":
    #         color = (0, 153, 255)
    #     elif color_type == "RCT":
    #         color = (255, 82, 141)
    #     else:
    #         color = (255, 0, 0)
    #     self.outline = "#%02x%02x%02x" % color
    #     self.canvas.delete(self.rect)
    #     self.rect = None

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

        self.canvas_top.grid()

    def create_canvas(self):
        self.select = Button(
            self.master, text="select an image", command=self.select_image)
        self.select.grid()

        my_frame = LabelFrame(self.master, text='Image')
        self.canvas = Canvas(my_frame, width=400,
                             height=400, bg="grey", cursor="cross")

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Configure>", lambda e: self.canvas.config(
            scrollregion=self.canvas.bbox("all")))

        self.canvas.grid(sticky='nesw')
        my_scrollbary = Scrollbar(my_frame)
        my_scrollbarx = Scrollbar(my_frame, orient="horizontal")
        my_scrollbary.grid(row=0, column=1, sticky='nse')
        my_scrollbarx.grid(row=1, column=0, sticky='new')
        my_frame.grid(sticky='nsew')

        my_scrollbary.configure(command=self.canvas.yview)
        my_scrollbarx.configure(command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=my_scrollbary.set)
        self.canvas.configure(xscrollcommand=my_scrollbarx.set)

    def create_categories(self):
        cat_frame = Frame(self.master)
        cat_frame.columnconfigure(1, weight=1)
        self.categories = ['Not Exposed', 'Exposed',
                           'Periapical', 'Bone Loss', 'RCT']
        self.cat_var = StringVar(cat_frame)
        self.cat_var.set(self.categories[0])
        cat_label = Label(cat_frame, text='Category: ')
        cat_label.grid(sticky=E + W, padx=5, pady=5)
        self.cat_inp = OptionMenu(cat_frame, self.cat_var, *self.categories)
        self.cat_inp.grid(row=0, column=1, sticky=E + W, padx=5, pady=5)
        cat_frame.grid(sticky='ew')
        self.cat_var.trace("w", self.outline_change)

    def create_box_list(self):
        box_list_frame = Frame(self.master)
        box_list_frame.columnconfigure(0, weight=1)
        self.box_list = {'': 0}
        self.box_list_var = StringVar(box_list_frame)
        self.box_list_inp = OptionMenu(
            box_list_frame, self.box_list_var, *self.box_list.keys())
        self.box_list_inp.grid(row=0, column=0, sticky=E + W, padx=5, pady=5)
        box_list_btn = Button(
            box_list_frame, text='Delete Box', command=self.delete_box_opt)
        box_list_btn.grid(row=0, column=1, sticky=E + W, padx=5, pady=5)
        box_list_frame.grid(sticky='ew')
        # self.box_list_var.trace("w", self.delete_box_opt)

    def outline_change(self, *args):
        color_type = self.cat_var.get()
        if color_type == "Not Exposed":
            color = (255, 0, 0)
        elif color_type == "Exposed":
            color = (0, 0, 255)
        elif color_type == "Periapical":
            color = (0, 255, 0)
        elif color_type == "Bone Loss":
            color = (0, 153, 255)
        elif color_type == "RCT":
            color = (255, 82, 141)
        else:
            color = (255, 0, 0)
        print(color_type)
        self.outline = "#%02x%02x%02x" % color
        self.canvas.delete(self.rect)
        self.rect = None

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        # create rectangle if not yet exist
        if not self.rect:
            self.rect = self.canvas.create_rectangle(
                self.x, self.y, 1, 1, outline=self.outline, width=3)

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
            coordinates, outline=self.outline, width=3)
        # print(self.canvas.coords(cek))
        self.num_list.insert(0, str(cek))
        self.cat[self.cat_var.get()] += 1
        self.box_list[f"{self.cat_var.get()} {self.cat[self.cat_var.get()]}"] = cek
        self.recreate_box_list()

    def select_image(self):
        self.canvas.delete(self.num)
        file_path = filedialog.askopenfilename()
        des = Image.open(file_path)
        bg_image = ImageTk.PhotoImage(des)
        self.canvas.bg_image = bg_image
        cek = self.canvas.create_image(
            0, 0, anchor="nw", image=self.canvas.bg_image)

        self.num = cek

    # def on_click(self):
    #     coordinates = 50, 0, 100, 50
    #     self.canvas.create_rectangle(
    #         coordinates, outline=self.outline, width=3)
        # color change
        # self.num += 1
        # self.num_list.insert(0, self.num)

    # def delete_box(self):
        # self.canvas.delete("all")
        # if len(self.num_list) > 0:
        #     if self.rect and self.num_list[0] < self.rect:
        #         self.canvas.delete(self.rect)
        #         self.rect = None
        #     else:
        #         self.canvas.delete(self.num_list[0])
        #         self.num_list.pop(0)
        # elif self.rect and len(self.num_list) == 0:
        #     self.canvas.delete(self.rect)
        #     self.rect = None

    def delete_image(self):
        if self.num > 0:
            self.canvas.delete(self.num)
            self.num = 0

    def delete_box_opt(self):
        if self.box_list_var.get() == '' or self.box_list_var.get() == ' ':
            return
        get_index = self.num_list.index(
            str(self.box_list[self.box_list_var.get()]))
        self.canvas.delete(
            self.num_list[get_index])
        self.num_list.pop(get_index)
        self.box_list.pop(self.box_list_var.get())
        self.recreate_box_list()

    def recreate_box_list(self):
        menu = self.box_list_inp["menu"]
        menu.delete(0, "end")
        for string in self.box_list.keys():
            menu.add_command(label=string,
                             command=lambda value=string: self.box_list_var.set(value))
        self.box_list_var.set(" ")

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
    # root.resizable(0, 0)
    my_gui = Gui(root)
    root.call('wm', 'attributes', '.', '-topmost', '1')
    # root.overrideredirect(True)
    root.mainloop()
