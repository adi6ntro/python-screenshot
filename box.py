from datetime import datetime
from functools import partial
from PIL import Image, ImageTk
from sys import platform
from tkinter import Tk, filedialog, Frame, Button, Canvas, Label, Entry, LabelFrame, Scrollbar, Text, StringVar, OptionMenu, messagebox, E, W, Y, X, BOTH, LEFT, RIGHT, BOTTOM, VERTICAL, DISABLED
from ttkbootstrap.constants import *
import cv2
import io
import pyscreenshot as ImageGrab
import os
import save_var
import ttkbootstrap as ttk
import utils.ApiClass as ac
import webbrowser

os.environ["PATH"] += ":/usr/local/bin/gs"


class Gui(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
    #     button1 = Button(self, text="Go to Page One",
    #                         command=lambda: controller.show_frame("PageOne"))
    #     button2 = Button(self, text="Go to Page Two",
    #                         command=lambda: controller.show_frame("PageTwo"))
        self.num_list = []
        self.box_delete = {}
        self.url_id = ''
        self.cat = {
            "Exposed": {'type': 1, 'num': 0},
            "Not Exposed": {'type': 2, 'num': 0},
            "Periapical": {'type': 3, 'num': 0},
            "Bone Loss": {'type': 4, 'num': 0},
            "RCT": {'type': 5, 'num': 0},
            "Other": {'type': 6, 'num': 0}
        }
        self.cat_type = {
            1: "Exposed",
            2: "Not Exposed",
            3: "Periapical",
            4: "Bone Loss",
            5: "RCT",
            6: "Other"
        }
        self.doctor_id = 10
        self.num = 0
        self.x = self.y = 0
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.outline = "#%02x%02x%02x" % (255, 0, 0)
        self.lines = []
        self.init_frame()
        self.screenshot_widgets()
        self.create_canvas()
        self.create_btn()
        self.create_patients()
        self.create_categories()
        self.create_box_list()

    def init_frame(self):
        self.frame = Frame(self)
        self.frame.pack(fill=BOTH, expand=1)
        self.master_canvas = Canvas(
            self.frame, width=save_var.screen_width, height=save_var.screen_height)
        self.master_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        master_scrollbar = Scrollbar(
            self.frame, orient=VERTICAL, command=self.master_canvas.yview)
        master_scrollbar.pack(side=RIGHT, fill=Y)
        self.master_canvas.configure(yscrollcommand=master_scrollbar.set)
        self.master_canvas.bind('<Configure>', lambda e: self.master_canvas.configure(
            scrollregion=self.master_canvas.bbox("all")))

    def screenshot_widgets(self):
        ss_frame = Frame(self.master_canvas, padx=20, pady=20)
        self.master_canvas.create_window(
            (200, 0), window=ss_frame)
        self.canvas_top = Frame(ss_frame)
        image1 = Image.open("swc.ico")
        my_img1 = ImageTk.PhotoImage(image1.resize((30, 30)))

        self.logo = Label(ss_frame, image=my_img1)
        self.logo.grid(sticky=E+W)
        self.logo.img_ref = my_img1

        fs_button = Button(ss_frame, text="Take Full Screen",
                           command=partial(self.hide_window),
                           bg="#8e936d", fg="black", padx=10,
                           #    bootstyle=(SUCCESS, OUTLINE)
                           font=("Sans Serif", 9)
                           )
        fs_button.grid()

        self.label = Entry(ss_frame, font=('helvetica', 10),
                           bd=0, width=50, justify='center')
        self.label.grid(sticky=E+W)

        self.canvas_top.grid()

    def create_btn(self):
        self.ebox_frame = Frame(self.master_canvas, padx=20, pady=20)
        self.master_canvas.create_window(
            (200, 230), window=self.ebox_frame)
        btn = Frame(self.ebox_frame)
        self.select = Button(
            btn, text="Open report", command=self.select_image)  # , bootstyle="info"
        self.select.grid(row=0, column=0)
        self.del_img = Button(btn, text="Reset report",
                              command=self.delete_image)  # , bootstyle="danger"
        self.del_img.grid(row=0, column=1)
        btn.grid()

    def create_canvas(self):
        self.canvas_frame = Frame(self.master_canvas)
        # width = round(save_var.screen_width * 20 / 100)
        # height = round(save_var.screen_height * 30 / 100)
        self.master_canvas.create_window(
            # (width, height), window=self.canvas_frame)
            (900, 330), window=self.canvas_frame)
        # (500, 100), window=self.canvas_frame)
        self.my_frame = LabelFrame(self.canvas_frame, text='Report Image')
        # print(width)
        # print(height)
        self.canvas = Canvas(self.my_frame, width=960,
                             height=720, bg="grey", cursor="cross")

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Configure>", lambda e: self.canvas.config(
            scrollregion=self.canvas.bbox("all")))

        my_scrollbary = Scrollbar(self.my_frame)
        my_scrollbarx = Scrollbar(self.my_frame, orient="horizontal")
        my_scrollbary.pack(side=RIGHT, fill=Y)
        my_scrollbarx.pack(side=BOTTOM, fill=X)
        self.canvas.pack(fill=BOTH, expand=True)
        self.my_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        my_scrollbary.configure(command=self.canvas.yview)
        my_scrollbarx.configure(command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=my_scrollbary.set)
        self.canvas.configure(xscrollcommand=my_scrollbarx.set)

    def create_patients(self):
        patients_frame = Frame(self.ebox_frame)
        patients_frame.columnconfigure(1, weight=1)
        self.patients_var = StringVar(patients_frame)
        self.patients_var.set(save_var.patients[0])
        patients_label = Label(patients_frame, text='Patient: ')
        patients_label.grid(sticky=E + W, padx=5, pady=5)
        self.patients_inp = OptionMenu(
            patients_frame, self.patients_var, *save_var.patients)
        self.patients_inp.grid(row=0, column=1, sticky=E + W, padx=5, pady=5)
        patients_frame.grid(sticky='ew')

    def create_categories(self):
        cat_frame = Frame(self.ebox_frame)
        cat_frame.columnconfigure(1, weight=1)
        self.categories = ['Exposed', 'Not Exposed',
                           'Periapical', 'Bone Loss', 'RCT', 'Other']
        self.cat_var = StringVar(cat_frame)
        self.cat_var.set(self.categories[0])
        cat_label = Label(cat_frame, text='Category: ')
        cat_label.grid(sticky=E + W, padx=5, pady=5)
        self.cat_inp = OptionMenu(
            cat_frame, self.cat_var, *self.categories)
        self.cat_inp.grid(row=0, column=1, sticky=E + W, padx=5, pady=5)
        cat_frame.grid(sticky='ew')
        self.cat_var.trace("w", self.outline_change)

    def create_box_list(self):
        box_list_frame = Frame(self.ebox_frame)
        box_list_frame.columnconfigure(1, weight=1)
        self.box_list = {
            ' ': {
                'canvas_id': 0,
                'box_type': 0,
                'box_num': 0,
                'coordinate': [0, 0, 0, 0],
                'confidence': "",
                'distance': "",
                'overlap': "",
            }
        }
        self.box_list_var = StringVar(box_list_frame)
        box_list_label = Label(box_list_frame, text='Box List: ')
        box_list_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.box_list_inp = OptionMenu(
            box_list_frame, self.box_list_var, *self.box_list.keys())
        self.box_list_inp.grid(row=0, column=1, sticky=E + W, padx=5, pady=5)
        self.box_list_var.trace("w", self.box_list_change)

        coordinate_label = Label(box_list_frame, text='Coordinate: ')
        coordinate_label.grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.coordinate_str = StringVar(box_list_frame)
        self.coordinate_str.set('0,0,0,0')
        self.coordinate_ent = Entry(box_list_frame,
                                    textvariable=self.coordinate_str, state=DISABLED)
        self.coordinate_ent.grid(row=1, column=1, sticky=E + W, padx=5, pady=5)

        confidence_label = Label(box_list_frame, text='Confidence: ')
        confidence_label.grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.confidence_str = StringVar(box_list_frame)
        self.confidence_str.set('')
        self.confidence_ent = Entry(box_list_frame,
                                    textvariable=self.confidence_str)
        self.confidence_ent.grid(row=2, column=1, sticky=E + W, padx=5, pady=5)

        distance_label = Label(box_list_frame, text='Distance: ')
        distance_label.grid(row=3, column=0, sticky=W, padx=5, pady=5)
        self.distance_str = StringVar(box_list_frame)
        self.distance_str.set('')
        self.distance_ent = Entry(box_list_frame,
                                  textvariable=self.distance_str)
        self.distance_ent.grid(row=3, column=1, sticky=E + W, padx=5, pady=5)

        overlap_label = Label(box_list_frame, text='overlap: ')
        overlap_label.grid(row=4, column=0, sticky=W, padx=5, pady=5)
        self.overlap_str = StringVar(box_list_frame)
        self.overlap_str.set('')
        self.overlap_ent = Entry(box_list_frame,
                                 textvariable=self.overlap_str)
        self.overlap_ent.grid(row=4, column=1, sticky=E + W, padx=5, pady=5)

        box_list_btn_update = Button(
            box_list_frame, text='Update Box', command=self.update_box_opt)  # , bootstyle="danger"
        box_list_btn_update.grid(row=5, column=0, sticky=W, padx=5, pady=5)
        box_list_btn_delete = Button(
            box_list_frame, text='Delete Box', command=self.delete_box_opt)  # , bootstyle="danger"
        box_list_btn_delete.grid(row=5, column=1, sticky=W, padx=5, pady=5)

        create_report_btn = Button(
            box_list_frame, text='Create New Report', command=self.generate_report)  # , bootstyle="danger"
        create_report_btn.grid(
            row=6, column=0, columnspan=2, sticky=W, padx=5, pady=5)
        open_report_btn = Button(
            box_list_frame, text='Download New Report', command=self.open_report)  # , bootstyle="danger"
        open_report_btn.grid(
            row=7, column=0, columnspan=2, sticky=W, padx=5, pady=5)
        box_list_frame.grid(sticky='ew')

    def outline_change(self, *args):
        color_type = self.cat_var.get()
        self.color_type(color_type)
        self.canvas.delete(self.rect)
        self.rect = None

    def color_type(self, color_type):
        if color_type == "Exposed":
            color = (255, 0, 0)
        elif color_type == "Not Exposed":
            color = (0, 0, 255)
        elif color_type == "Periapical":
            color = (0, 255, 0)
        elif color_type == "Bone Loss":
            color = (255, 153, 0)
        elif color_type == "RCT":
            color = (141, 82, 255)
        else:
            color = (255, 0, 0)
        self.outline = "#%02x%02x%02x" % color

    def box_list_change(self, *args):
        # if self.box_list_var.get() == ' ':
        #     self.box_list_var.set(" ")
        self.coordinate_str.set(
            self.box_list[self.box_list_var.get()]['coordinate'])
        self.confidence_str.set(
            self.box_list[self.box_list_var.get()]['confidence'])
        self.distance_str.set(
            self.box_list[self.box_list_var.get()]['distance'])
        self.overlap_str.set(self.box_list[self.box_list_var.get()]['overlap'])

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

        cek = self.canvas.create_rectangle(
            coordinates, outline=self.outline, width=3)

        self.num_list.insert(0, str(cek))
        self.cat[self.cat_var.get()]['num'] += 1

        self.box_list[f"{self.cat_var.get()} {self.cat[self.cat_var.get()]['num']}"] = {
        }
        self.box_list[f"{self.cat_var.get()} {self.cat[self.cat_var.get()]['num']}"]['canvas_id'] = cek
        self.box_list[f"{self.cat_var.get()} {self.cat[self.cat_var.get()]['num']}"]['box_type'] = self.cat[self.cat_var.get()]['type']
        self.box_list[f"{self.cat_var.get()} {self.cat[self.cat_var.get()]['num']}"]['box_num'] = self.cat[self.cat_var.get(
        )]['num'] - 1
        self.box_list[f"{self.cat_var.get()} {self.cat[self.cat_var.get()]['num']}"]['coordinate'] = list(
            coordinates)
        self.box_list[f"{self.cat_var.get()} {self.cat[self.cat_var.get()]['num']}"]['confidence'] = ""
        self.box_list[f"{self.cat_var.get()} {self.cat[self.cat_var.get()]['num']}"]['distance'] = ""
        self.box_list[f"{self.cat_var.get()} {self.cat[self.cat_var.get()]['num']}"]['overlap'] = ""

        self.recreate_box_list()

    def select_image(self):
        self.canvas.delete("all")
        file_path = filedialog.askopenfilename()

        apiObj = ac.ApiClass()
        response = apiObj.aitools(
            file_path, save_var.email, save_var.token, "1")
        if response['code'] != '00':
            messagebox.showerror(title="Error", message=response['message'])
            return

        self.des = Image.open(file_path)
        bg_image = ImageTk.PhotoImage(self.des)
        # bg_image = bg_image._PhotoImage__photo.subsample(2)
        self.canvas.bg_image = bg_image
        img = cv2.imread(file_path)
        dh, dw, _ = img.shape
        self.img_width = bg_image.width()
        self.img_height = bg_image.height()
        # dw = bg_image.width()
        # dh = bg_image.height()
        cek = self.canvas.create_image(
            0, 0, anchor="nw", image=bg_image)
        # self.canvas.place(x=0, y=0, height=bg_image.height(),
        #                   width=bg_image.width())

        self.num = cek

        last_val = self.box_list[' ']
        self.box_list.clear()
        self.num_list.clear()
        self.box_list[' '] = last_val

        coordinate_exposed = "" if response['data']['exposed_pulp_box_position'] == "" or response['data'][
            'exposed_pulp_box_position'] == "-" else response['data']['exposed_pulp_box_position'].split('&')
        confidence_exposed = "" if response['data']['exposed_pulp_confidence'] == "" or response['data'][
            'exposed_pulp_confidence'] == "-" else response['data']['exposed_pulp_confidence'].split('&')
        distance_exposed = "" if response['data']['exposed_pulp_distance'] == "" or response['data'][
            'exposed_pulp_distance'] == "-" else response['data']['exposed_pulp_distance'].split('&')
        overlap_exposed = "" if response['data']['exposed_pulp_overlap'] == "" or response['data'][
            'exposed_pulp_overlap'] == "-" else response['data']['exposed_pulp_overlap'].split('&')
        self.get_box_data(1, coordinate_exposed, (dh, dw),
                          confidence_exposed, distance_exposed, overlap_exposed)

        coordinate_non_exposed = "" if response['data']['non_exposed_pulp_box_position'] == "" or response['data'][
            'non_exposed_pulp_box_position'] == "-" else response['data']['non_exposed_pulp_box_position'].split('&')
        confidence_non_exposed = "" if response['data']['non_exposed_pulp_confidence'] == "" or response['data'][
            'non_exposed_pulp_confidence'] == "-" else response['data']['non_exposed_pulp_confidence'].split('&')
        distance_non_exposed = "" if response['data']['non_exposed_pulp_distance'] == "" or response['data'][
            'non_exposed_pulp_distance'] == "-" else response['data']['non_exposed_pulp_distance'].split('&')
        overlap_non_exposed = "" if response['data']['non_exposed_pulp_overlap'] == "" or response['data'][
            'non_exposed_pulp_overlap'] == "-" else response['data']['non_exposed_pulp_overlap'].split('&')
        self.get_box_data(2, coordinate_non_exposed, (dh, dw),
                          confidence_non_exposed, distance_non_exposed, overlap_non_exposed)

        coordinate_periapical = "" if response['data']['periapical_lesion_box_position'] == "" or response['data'][
            'periapical_lesion_box_position'] == "-" else response['data']['periapical_lesion_box_position'].split('&')
        confidence_periapical = "" if response['data']['periapical_lesion_confidence'] == "" or response['data'][
            'periapical_lesion_confidence'] == "-" else response['data']['periapical_lesion_confidence'].split('&')
        distance_periapical = "" if response['data']['periapical_lesion_distance'] == "" or response['data'][
            'periapical_lesion_distance'] == "-" else response['data']['periapical_lesion_distance'].split('&')
        overlap_periapical = "" if response['data']['periapical_lesion_overlap'] == "" or response['data'][
            'periapical_lesion_overlap'] == "-" else response['data']['periapical_lesion_overlap'].split('&')
        self.get_box_data(3, coordinate_periapical, (dh, dw),
                          confidence_periapical, distance_periapical, overlap_periapical)

        coordinate_bone_loss = "" if response['data']['bone_loss_box_position'] == "" or response['data'][
            'bone_loss_box_position'] == "-" else response['data']['bone_loss_box_position'].split('&')
        confidence_bone_loss = "" if response['data']['bone_loss_confidence'] == "" or response['data'][
            'bone_loss_confidence'] == "-" else response['data']['bone_loss_confidence'].split('&')
        distance_bone_loss = "" if response['data']['bone_loss_distance'] == "" or response['data'][
            'bone_loss_distance'] == "-" else response['data']['bone_loss_distance'].split('&')
        overlap_bone_loss = "" if response['data']['bone_loss_overlap'] == "" or response['data'][
            'bone_loss_overlap'] == "-" else response['data']['bone_loss_overlap'].split('&')
        self.get_box_data(4, coordinate_bone_loss, (dh, dw),
                          confidence_bone_loss, distance_bone_loss, overlap_bone_loss)

        coordinate_root_canal = "" if response['data']['root_canal_box_position'] == "" or response['data'][
            'root_canal_box_position'] == "-" else response['data']['root_canal_box_position'].split('&')
        confidence_root_canal = "" if response['data']['root_canal_confidence'] == "" or response['data'][
            'root_canal_confidence'] == "-" else response['data']['root_canal_confidence'].split('&')
        distance_root_canal = "" if response['data']['root_canal_distance'] == "" or response['data'][
            'root_canal_distance'] == "-" else response['data']['root_canal_distance'].split('&')
        overlap_root_canal = "" if response['data']['root_canal_overlap'] == "" or response['data'][
            'root_canal_overlap'] == "-" else response['data']['root_canal_overlap'].split('&')
        self.get_box_data(5, coordinate_root_canal, (dh, dw),
                          confidence_root_canal, distance_root_canal, overlap_root_canal)

        self.recreate_box_list()

    def get_box_data(self, tipe, coordinate, d, confidence, distance, overlap):
        dh, dw = d
        if coordinate == "":
            return

        for idx, row in enumerate(coordinate):
            # Split string to float
            x, y, w, h = map(float, row.split(' '))

            # Taken from https://github.com/pjreddie/darknet/blob/810d7f797bdb2f021dbe65d2524c2ff6b8ab5c8b/src/image.c#L283-L291
            # via https://stackoverflow.com/questions/44544471/how-to-get-the-coordinates-of-the-bounding-box-in-yolo-object-detection#comment102178409_44592380
            l = int((x - w / 2) * dw)
            r = int((x + w / 2) * dw)
            t = int((y - h / 2) * dh)
            b = int((y + h / 2) * dh)

            if l < 0:
                l = 0
            if r > dw - 1:
                r = dw - 1
            if t < 0:
                t = 0
            if b > dh - 1:
                b = dh - 1
            coordinates = (l, t, r, b)
            self.color_type(self.cat_type[int(tipe)])
            cek = self.canvas.create_rectangle(
                coordinates, outline=self.outline, width=3)

            self.num_list.insert(0, str(cek))
            self.cat[self.cat_type[int(tipe)]]['num'] += 1
            self.box_list[f"{self.cat_type[int(tipe)]} {self.cat[self.cat_type[int(tipe)]]['num']}"] = {
            }
            self.box_list[f"{self.cat_type[int(tipe)]} {self.cat[self.cat_type[int(tipe)]]['num']}"]['canvas_id'] = cek
            self.box_list[f"{self.cat_type[int(tipe)]} {self.cat[self.cat_type[int(tipe)]]['num']}"]['box_type'] = int(
                tipe)
            self.box_list[f"{self.cat_type[int(tipe)]} {self.cat[self.cat_type[int(tipe)]]['num']}"][
                'box_num'] = self.cat[self.cat_type[int(tipe)]]['num'] - 1
            self.box_list[f"{self.cat_type[int(tipe)]} {self.cat[self.cat_type[int(tipe)]]['num']}"]['coordinate'] = list(
                coordinates)
            self.box_list[f"{self.cat_type[int(tipe)]} {self.cat[self.cat_type[int(tipe)]]['num']}"]['confidence'] = confidence[idx]
            self.box_list[f"{self.cat_type[int(tipe)]} {self.cat[self.cat_type[int(tipe)]]['num']}"][
                'distance'] = distance[idx] if tipe != 5 and distance != "" else ""
            self.box_list[f"{self.cat_type[int(tipe)]} {self.cat[self.cat_type[int(tipe)]]['num']}"][
                'overlap'] = overlap[idx] if tipe != 5 and overlap != "" else ""

        if tipe == 5:
            if distance != "":
                for idx, row in enumerate(distance):
                    x = row.split('-')
                    self.box_list[f"{self.cat_type[int(tipe)]} {x[0]}"]['distance'] = x[1]

            if overlap != "":
                for idx, row in enumerate(overlap):
                    x = row.split('-')
                    self.box_list[f"{self.cat_type[int(tipe)]} {x[0]}"]['overlap'] = 'Yes'

    def delete_image(self):
        self.canvas.delete("all")
        self.num = 0
        last_val = self.box_list[' ']
        self.box_list.clear()
        self.num_list.clear()
        self.box_list[' '] = last_val
        self.recreate_box_list()

    def delete_box_opt(self):
        if self.box_list_var.get() == '' or self.box_list_var.get() == ' ':
            return
        get_index = self.num_list.index(
            str(self.box_list[self.box_list_var.get()]['canvas_id']))
        self.canvas.delete(
            self.num_list[get_index])
        self.num_list.pop(get_index)
        self.box_list.pop(self.box_list_var.get())
        self.recreate_box_list()

    def update_box_opt(self):
        if self.box_list_var.get() == '' or self.box_list_var.get() == ' ':
            return
        confidence = self.confidence_str.get()
        distance = self.distance_str.get()
        overlap = self.overlap_str.get()
        self.box_list[self.box_list_var.get()]['confidence'] = confidence
        self.box_list[self.box_list_var.get()]['distance'] = distance
        self.box_list[self.box_list_var.get()]['overlap'] = overlap
        self.recreate_box_list()

    def recreate_box_list(self):
        menu = self.box_list_inp["menu"]
        menu.delete(0, "end")
        for string in self.box_list.keys():
            menu.add_command(label=string,
                             command=lambda value=string: self.box_list_var.set(value))
        self.box_list_var.set(" ")

    def generate_report(self):
        image_name = "new_image/" + \
            str(datetime.now()).replace(" ", "").replace(":", "") + ".jpg"
        self.canvas.config(height=self.img_height,
                           width=self.img_width)
        self.canvas.update()
        ps = self.canvas.postscript(colormode='color')
        psimage = Image.open(io.BytesIO(ps.encode('utf-8')))
        psimage.save(image_name)
        self.canvas.config(width=960, height=720)
        self.my_frame.config(width=960, height=720)
        self.canvas_frame.config(width=960, height=720)
        arr = {
            "email": save_var.email,
            "token": save_var.token,
            "patient": self.patients_var.get(),
            'box_data': []
        }
        for row in self.box_list:
            if row == ' ':
                continue
            dw = 1./self.img_width
            dh = 1./self.img_height
            box = self.box_list[row]['coordinate']
            x = (box[0] + box[2])/2.0
            y = (box[1] + box[3])/2.0
            w = box[2] - box[0]
            h = box[3] - box[1]
            x = x*dw
            y = y*dh
            w = w*dw
            h = h*dh
            # self.box_list[row]['coordinate'] = [x, y, w, h]
            self.box_list[row]['coordinate'] = f"{x} {y} {w} {h}"
            arr['box_data'].append(self.box_list[row])

        apiObj = ac.ApiClass()
        response = apiObj.update_report(arr)
        if response:
            self.delete_image()

    def open_report(self):
        webbrowser.open_new_tab("https://swc-dent.com/"+self.url_id)

    def clip_screen(self):
        # self.master.withdraw()
        image_name = "snips/" + \
            str(datetime.now()).replace(" ", "").replace(":", "") + ".png"
        try:
            image = ImageGrab.grab(childprocess=False)
            image.save(image_name, format='PNG', subsampling=0, quality=100)
            img = Image.open(image_name)
            resized = img.resize((30, 30), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(resized)
            self.logo.configure(image=photo)
            self.canvas_top.create_window(150, 20, window=self.logo)

        except Exception as e:
            print(e)
            return e
        self.deiconify()
        my_path = os.path.abspath(image_name)
        return f"{my_path}"

    def hide_window(self):
        self.withdraw()
        self.after(1000, self.get_fullscreen)

    def get_fullscreen(self):
        my_path = self.clip_screen()
        self.label.insert(0, my_path)
        self.label.config(bd=0, state='readonly')
        if platform == "win32":
            os.system(my_path)
