from tkinter import *
from tkinter import ttk

root = Tk()
root.title("SWC Screenshot App")
root.iconbitmap("swc.ico")
root.geometry("500x400")

main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

my_scrollbar = ttk.Scrollbar(
    main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(
    scrollregion=my_canvas.bbox("all")))

second_frame = Frame(my_canvas)

my_canvas.create_window((0, 0), window=second_frame, anchor="nw")


# for thing in range(100):
#     Button(second_frame, text=f'Button {thing} Yo!').grid(
#         row=thing, column=0, padx=10, pady=10)


hidden = True


def label_hide_show(btn, text):
    global hidden
    if hidden:
        label1.config(text=text)  # Change to passed text
        label1.grid(row=2, column=0, padx=10, pady=10)  # Pack it after the btn
        hidden = False
    else:
        label1.grid_forget()
        hidden = True
    print(hidden)


label1 = Label(second_frame)
btn1 = Button(second_frame, text="Get Started", height=3, width=26, bg="White",
              fg="Black", command=lambda: label_hide_show(btn1, 'Label below one')).grid(row=0, column=0, padx=10, pady=10)
btn2 = Button(second_frame, text="Collaborate", height=3, width=26, bg="White",
              fg="Black", command=lambda: label_hide_show(btn2, 'Label below two')).grid(row=1, column=0, padx=10, pady=10)


root.mainloop()
