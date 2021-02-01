import tkinter as tk
from requests import exceptions
import threading
import time
import datetime
import sys

# GUI
HEIGHT = 300
WIDTH = 400
TITLE = "Auto Refresher Refreshing"
# Refresher
MAX_DAYS_DELTA = 5
INTERNET_CONNECTION_ERR_SLEEP_TIME = 10
# HTML parser
COURSE_NAME_HTML_INDEX = 0
COURSE_GRADE_HTML_INDEX = 2
COURSE_DATE_HTML_INDEX = 3

refresh_count = 1


# get string convert it to Date object if possible
def convert_str_to_date(str_date):
    day = 0
    if str_date[0] != '0':
        day = int(str_date[0:2])
    else:
        day = int(str_date[1:2])
    month = 0
    if str_date[3] != '0':
        month = int(str_date[3:5])
    else:
        month = int(str_date[4:5])
    year = int(str_date[6:])
    date = datetime.date(year, month, day)
    del day, month, year
    return date


# for MOADY BET
def is_grade_new(manager, course_name):
    today = datetime.date.today()

    manager.browser.open("https://inbar.biu.ac.il/Live/Main.aspx")
    page_html = manager.browser.parsed
    grade_block = page_html.find_all("div", {"id": "ContentPlaceHolder1_dvStudentGradesList"})[0]
    for course_html in grade_block.find_all("tr"):
        name_str = course_html.find_all("td")[COURSE_NAME_HTML_INDEX].text
        date_str = course_html.find_all("td")[COURSE_DATE_HTML_INDEX].text
        if name_str == course_name:
            delta_time = today - convert_str_to_date(date_str)
            del today, page_html, grade_block, name_str, date_str
            return int(delta_time.days) < MAX_DAYS_DELTA
        del name_str, date_str

    del today, page_html, grade_block


# entry point
def start_refresher(manager):
    global refresh_count

    manager.init_window(WIDTH, HEIGHT, TITLE)

    # msg frame
    frame = tk.Frame(manager.window, bg=manager.window_bg, bd=10)
    frame.place(relwidth=1, relheight=1)

    # msg label
    msg1_label = tk.Label(frame, text="Wishing for the best 🤞🤞", bg=manager.window_bg, font=70, fg='green')
    msg1_label.place(anchor='n', relx=0.5, rely=0.1, relwidth=1, relheight=0.2)

    count_str = tk.StringVar()
    count_label = tk.Label(frame, textvariable=count_str, bg=manager.window_bg, font=200, fg='red')
    count_label.place(anchor='n', relx=0.5, rely=0.4, relwidth=1, relheight=0.2)
    count_str.set("Attempt count: " + str(refresh_count))

    msg = tk.StringVar()
    update_label = tk.Label(frame, textvariable=msg, bg=manager.window_bg, font=200, fg='green')
    update_label.place(anchor='n', relx=0.5, rely=0.7, relwidth=1, relheight=0.2)
    msg.set("You can go back to netflix \n we will take it from here (☞ﾟヮﾟ)☞")

    def check_for_grades():
        # open page
        manager.browser.open("https://inbar.biu.ac.il/Live/Login.aspx")
        login_form = manager.browser.get_form()
        login_form['edtUsername'] = manager.user.username
        login_form['edtPassword'] = manager.user.password
        manager.browser.submit_form(login_form)
        # open grades page
        manager.browser.open("https://inbar.biu.ac.il/live/StudentGradesList.aspx")

        page_html = manager.browser.parsed
        courses = page_html.find_all("tr", {"id": "ContentPlaceHolder1_gvGradesList"})
        for course in courses:
            course_index = course.contents[1].contents[1].attrs['id'][45:]
            course_code_id = "ContentPlaceHolder1_gvGradesList_lblUserCode_" + course_index
            course_code = course.find_all("span", {"id": course_code_id})[0].text
            for user_course_code in manager.user.courses_list:
                if course_code in user_course_code or user_course_code in course_code:
                    course_grade_id = "ContentPlaceHolder1_gvGradesList_lblRowFinalGrade_" + course_index
                    grade = course.find_all("span", {"id": course_grade_id})[0].text
                    if grade != '':
                        course_name = course.contents[2].contents[0]
                        if is_grade_new(manager, course_name):
                            return course_name, grade
                        del course_name
                    del course_grade_id, grade
            del course_index, course_code_id, course_code
        del login_form, page_html, courses
        return "None", "None"

    def refresh():
        global refresh_count
        # refresh
        try:
            # checks for new grade
            the_name, the_grade = check_for_grades()
            if the_grade != "None" or the_name != "None":
                frame.destroy()
                new_grade(manager, the_name, the_grade)
            else:
                refresh_count += 1
                count_str.set("Attempt count: " + str(refresh_count))
                del the_name, the_grade
        # in case there is no internet connection
        except exceptions.ConnectionError:
            frame.destroy()
            connection_error(manager)

    def refresh_mainloop():
        while True:
            refresh()
            time.sleep(1 / manager.user.frequency * 60 * 60)

    manager.refresh_thread = threading.Thread(target=refresh_mainloop, args=())
    manager.refresh_thread.daemon = True
    manager.refresh_thread.start()


def new_grade(manager, name, grade):
    manager.init_window(WIDTH + 50, HEIGHT, "New Grade!")

    frame = tk.Frame(manager.window, bg=manager.window_bg, bd=10)
    frame.place(relwidth=1, relheight=1)

    # label
    label = tk.Label(frame, text=f"New grade uploaded:\n{name}\n\ngrade: {grade}", bg=manager.window_bg, font=70, fg="green")
    label.place(anchor='n', relx=0.5, rely=0, relwidth=1, relheight=0.4)
    # exit button
    exit_button = tk.Button(frame, text="Exit", font='40', bg=manager.button_bg, command=sys.exit)
    exit_button.place(anchor='n', relx=0.5, rely=0.5, relwidth=0.8, relheight=0.4)

    def audio_mainloop():
        while True:
            manager.start_audio("win")
            time.sleep(5)

    thread = threading.Thread(target=audio_mainloop, args=())
    thread.daemon = True
    thread.start()


def connection_error(manager):
    manager.init_window(WIDTH, HEIGHT, "Connection Error")

    def resume():
        frame.destroy()
        del frame, error_label, resume_button
        start_refresher(manager)

    frame = tk.Frame(manager.window, bg=manager.window_bg, bd=10)
    frame.place(relwidth=1, relheight=1)
    # error label
    error_label = tk.Label(frame, text="There is no internet connection (⊙_⊙;)\nCheck your connection and try again"
                           , bg=manager.window_bg, font=70, fg="red")
    error_label.place(anchor='n', relx=0.5, rely=0, relwidth=1, relheight=0.3)
    # resume button
    resume_button = tk.Button(frame, text="Resume", font='40', bg=manager.button_bg, command=lambda: resume())
    resume_button.place(anchor='n', relx=0.5, rely=0.4, relwidth=0.8, relheight=0.5)
