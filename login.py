from tkinter import Frame, Label, Entry, Button, messagebox
import utils.ApiClass as ac
import save_var


class Login(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, padx=20, pady=20)
        # self.master = Frame(parent)
        self.controller = controller
        self.config(width=600, height=600)
        self.token = ''

        username_label = Label(
            self, text="Username", font=("Arial", 16))
        self.username_entry = Entry(self, font=("Arial", 16))
        self.password_entry = Entry(self, show="*", font=("Arial", 16))
        password_label = Label(
            self, text="Password", font=("Arial", 16))
        login_button = Button(
            self, text="Login", font=("Arial", 16), command=self.login)

        username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1, pady=10)
        password_label.grid(row=2, column=0)
        self.password_entry.grid(row=2, column=1, pady=10)
        login_button.grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        global token
        global name
        global email
        apiObj = ac.ApiClass()
        response = apiObj.login(self.username_entry.get(),
                                self.password_entry.get())
        if response['code'] != '00':
            messagebox.showerror(title="Error", message=response['message'])
        else:
            messagebox.showinfo(title="Login Success",
                                message="You successfully logged in.")
            save_var.name = response['data']['name']
            save_var.email = response['data']['email']
            save_var.token = response['data']['token']
            name = response['data']['name']
            email = response['data']['email']
            token = response['data']['token']
            self.controller.show_frame("Gui")

    # def show_token(self):
    #     return self.token


token = ''
name = ''
email = ''


# frame = Frame()

# Creating widgets
# login_label = Label(
#     frame, text="Login", font=("Arial", 30))
# username_label = Label(
#     frame, text="Username", font=("Arial", 16))
# username_entry = Entry(frame, font=("Arial", 16))
# password_entry = Entry(frame, show="*", font=("Arial", 16))
# password_label = Label(
#     frame, text="Password", font=("Arial", 16))
# login_button = Button(
#     frame, text="Login", font=("Arial", 16), command=login)

# Placing widgets on the screen
# login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
# username_label.grid(row=1, column=0)
# username_entry.grid(row=1, column=1, pady=10)
# password_label.grid(row=2, column=0)
# password_entry.grid(row=2, column=1, pady=10)
# login_button.grid(row=3, column=0, columnspan=2, pady=10)

# frame.pack()

# window.mainloop()
