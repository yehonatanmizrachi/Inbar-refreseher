import tkinter as tk
from Refresher import start_refresher

HEIGHT = 400
WIDTH = 500
TITLE = "Auto Refresher Courses List"


def start_courses_list(manager):
    def add_course(name, frame, entry):
        if name != '' and manager.user.courses_list.count(name) == 0:
            manager.user.courses_list.append(name)
            label_str = ""
            for course in manager.user.courses_list:
                label_str = label_str + course + '\n'

            # courses list label
            list_label = tk.Label(frame, text=label_str, bg='white', font=40)
            list_label.place(relx=0.1, rely=0.15, relwidth=0.5, relheight=0.8)

            entry.delete(0, 'end')

    def start_refreshing():
        if manager.user.courses_list.__len__() == 0:
            label = tk.Label(msg_frame, text="No courses were chosen", bg=manager.window_bg, fg='red', font=70)
            label.place(relwidth=1, relheight=1)
            return
        # start refresher
        msg_frame.destroy()
        courses_frame.destroy()
        lower_frame.destroy()

        start_refresher(manager)

    manager.init_window(WIDTH, HEIGHT, TITLE)
    # msg frame
    msg_frame = tk.Frame(manager.window, bg=manager.window_bg, bd=5)
    msg_frame.place(anchor='n', relx=0.5, rely=0.02, relwidth=0.95, relheight=0.15)
    # msg
    msg_label = tk.Label(msg_frame, text="Connected successfully!\nAdd the courses code with the group number!"
                         , bg=manager.window_bg, font=10)
    msg_label.place(relwidth=1, relheight=1)

    # courses input frame
    courses_frame = tk.Frame(manager.window, bg=manager.window_bg, bd=5)
    courses_frame.place(anchor='n', relx=0.5, rely=0.15, relwidth=0.95, relheight=0.1)
    # course name label
    course_name_label = tk.Label(courses_frame, text="Course code:", bg=manager.window_bg, font=70)
    course_name_label.place(anchor='n', relx=0.15, relwidth=0.3, relheight=1)
    # course name entry
    course_name_entry = tk.Entry(courses_frame, font=40)
    course_name_entry.place(relx=0.3, rely=0.1, relwidth=0.5, relheight=0.8)
    # courses list frame
    lower_frame = tk.Frame(manager.window, bg=manager.window_bg, bd=5)
    lower_frame.place(anchor='n', relx=0.5, rely=0.28, relwidth=0.95, relheight=0.7)
    # courses list headline label
    courses_list_headline_label = tk.Label(lower_frame, text="Courses list:", bg=manager.window_bg, font=40)
    courses_list_headline_label.place(relx=-0.013, rely=-0.45, relwidth=0.3, relheight=1)

    # courses list label
    courses_list_label = tk.Label(lower_frame, text="None", bg='white', font=40)
    courses_list_label.place(relx=0.1, rely=0.15, relwidth=0.5, relheight=0.8)

    # add course button
    add_course_button = tk.Button(courses_frame, text="Add", font='40', bg=manager.button_bg,
                                  command=lambda: add_course(course_name_entry.get(), lower_frame, course_name_entry))
    add_course_button.place(relx=0.83, rely=0, relwidth=0.15, relheight=1)

    # continue button
    continue_button = tk.Button(lower_frame, text="Continue", font='70', bg=manager.button_bg,
                                command=lambda: start_refreshing())
    continue_button.place(relx=0.63, rely=0.15, relwidth=0.3, relheight=0.8)
