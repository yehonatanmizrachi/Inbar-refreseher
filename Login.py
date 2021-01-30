from requests import exceptions
import tkinter as tk
from User import User
from CoursesList import start_courses_list

HEIGHT = 350
WIDTH = 420
TITLE = "Auto Refresher login"


def start_login(manager):

    def try_login(user_name, password):
        try:
            # open the browser
            manager.browser.open("https://inbar.biu.ac.il/Live/Login.aspx")
            # gets the login form and submit it
            login_form = manager.browser.get_form()
            login_form['edtUsername'] = user_name
            login_form['edtPassword'] = password
            manager.browser.submit_form(login_form)
            # in case that the user_name or the password is incorrect
            if manager.browser.url == "https://inbar.biu.ac.il/Live/Login.aspx":
                input_label = tk.Label(submit_frame, text="Incorrect ID or password. please try again",
                                       bg=manager.window_bg, fg='red', font=65)
                input_label.place(anchor='n', relx=0.5, rely=0.15, relwidth=1, relheight=0.2)
                return

            # connected successfully
            manager.user = User(user_name, password)
            submit_frame.destroy()
            start_courses_list(manager)

        except exceptions.ConnectionError:
            input_label = tk.Label(submit_frame, text="There is no internet connection\n Please connect and try again",
                                   bg=manager.window_bg, fg='red', font=40)
            input_label.place(anchor='n', relx=0.5, rely=0.15, relwidth=1, relheight=0.2)

    manager.init_window(WIDTH, HEIGHT, TITLE)

    submit_frame = tk.Frame(manager.window, bg=manager.window_bg, bd=10)
    submit_frame.place(relwidth=1, relheight=1)
    # welcome label
    welcome_label = tk.Label(submit_frame, text="Welcome to Inbar AutoRefresher3.0 ✪ ω ✪", bg=manager.window_bg, font=70)
    welcome_label.place(anchor='n', relx=0.5, rely=0, relwidth=1, relheight=0.2)
    # login label
    login_label = tk.Label(submit_frame, text="Please login", bg=manager.window_bg, font=70)
    login_label.place(anchor='n', relx=0.5, rely=0.15, relwidth=1, relheight=0.2)
    # ID label
    id_label = tk.Label(submit_frame, text="ID:", bg=manager.window_bg, font=20)
    id_label.place(anchor='w', relx=0.1, rely=0.4, relwidth=0.2, relheight=0.1)
    # ID entry
    id_entry = tk.Entry(submit_frame, font=40)
    id_entry.place(anchor='w', relx=0.4, rely=0.4, relwidth=0.5, relheight=0.1)
    # Password label
    password_label = tk.Label(submit_frame, text="Password:", bg=manager.window_bg, font=20)
    password_label.place(anchor='w', rely=0.6, relwidth=0.4, relheight=0.1)
    # Password entry
    password_entry = tk.Entry(submit_frame, font=40, show='*')
    password_entry.place(anchor='w', relx=0.4, rely=0.6, relwidth=0.5, relheight=0.1)
    # submit button
    submit_button = tk.Button(submit_frame, text="Submit", font='40',
                              command=lambda: try_login(id_entry.get(), password_entry.get()), bg=manager.button_bg)
    submit_button.place(anchor='n', relx=0.5, rely=0.8, relwidth=0.3, relheight=0.1)

    # start the application
    manager.window.mainloop()
