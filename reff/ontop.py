from tkinter import *

root = Tk()
root.title("app")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("550x250+%d+%d" % (screen_width/2-275, screen_height/2-125))
root.configure(background='gold')
# root.lift()

# root.attributes('-topmost', True)
# root.update()
# root.attributes('-topmost', False)

root.call('wm', 'attributes', '.', '-topmost', '1')

root.mainloop()
