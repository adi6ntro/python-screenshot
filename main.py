from tkinter import *               # python 3
from tkinter import font as tkfont
from box import Gui
from login import Login
import os
import save_var
from screeninfo import get_monitors


class SwcDesktopApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(
            family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login, Gui):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        for aFrame in self.frames:
            # this will make the widget invisible, but its grid options will be remembered
            self.frames[aFrame].grid_remove()
        frame = self.frames[page_name]
        frame.grid()

    def get_screenwidth(self):
        return save_var.screen_width

    def get_screenheight(self):
        return save_var.screen_height


if __name__ == "__main__":
    for m in get_monitors():
        save_var.screen_width = m.width
        save_var.screen_height = m.height
    if not (os.path.isdir("snips")):
        os.mkdir("snips")
    if not (os.path.isdir("new_image")):
        os.mkdir("new_image")

    app = SwcDesktopApp()
    app.title("SWC Screenshot App")
    app.iconbitmap("swc.ico")

    w = 320  # width for the Tk root
    h = 180  # height for the Tk root

    # get screen width and height
    save_var.screen_width = app.winfo_screenwidth()
    save_var.screen_height = app.winfo_screenheight()

    ws = save_var.screen_width  # width of the screen
    hs = save_var.screen_height  # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen
    # and where it is placed
    app.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # app.call('wm', 'attributes', '.', '-topmost', '1')
    # app = ttk.Window()
    # app.resizable(0, 0)
    # app.overrideredirect(True)
    app.mainloop()
