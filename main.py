from tkinter import *               # python 3
from tkinter import font as tkfont
from box import Gui
from login import Login
import os


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


if __name__ == "__main__":
    if not (os.path.isdir("snips")):
        os.mkdir("snips")
    if not (os.path.isdir("new_image")):
        os.mkdir("new_image")

    app = SwcDesktopApp()
    app.title("SWC Screenshot App")
    app.iconbitmap("swc.ico")
    app.call('wm', 'attributes', '.', '-topmost', '1')
    app.mainloop()
