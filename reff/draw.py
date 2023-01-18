# Import the required libraries
from tkinter import *

# Create an instance of tkinter frame or window
win = Tk()

# Set the size of the tkinter window
win.geometry("700x350")

# Define a function to delete the shape

num = 1


def on_click():
    global num
    canvas.delete(num)
    # canvas.delete("all")
    num += 1


# Create a canvas widget
canvas = Canvas(win, width=500, height=300)
canvas.pack()

# Add a line in canvas widget
# line = canvas.create_line(100, 200, 200, 35, fill="red", width=10)
# line2 = canvas.create_line(200, 100, 100, 35, fill="blue", width=10)
# line3 = canvas.create_line(200, 200, 200, 35, fill="green", width=10)
# line4 = canvas.create_line(100, 100, 100, 35, fill="yellow", width=10)
# line5 = canvas.create_rectangle(50, 0, 100, 50, outline='red', width=10)
# print(line)
# print(line2)
# print(line3)
# print(line4)
# print(line5)
canvas.create_line(100, 200, 200, 35, fill="red", width=10)
canvas.create_line(200, 100, 100, 35, fill="blue", width=10)
canvas.create_line(200, 200, 200, 35, fill="green", width=10)
canvas.create_line(100, 100, 100, 35, fill="yellow", width=10)
canvas.create_rectangle(50, 0, 100, 50, outline='red', width=10)

# Create a button to delete the button
Button(win, text="Delete Shape", command=on_click).pack()

win.mainloop()
