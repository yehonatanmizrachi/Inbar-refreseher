import tkinter as tk
from robobrowser import RoboBrowser
from requests import exceptions
import time
import winsound
import datetime
import smtplib

# GUI
HEIGHT = 300
WIDTH = 400
TITLE = "Auto Refresher refresher"
# Refresher
MAX_DAYS_DELTA = 10
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
    return datetime.date(year, month, day)


# entry point
def start_refresher(manager):
    global refresh_count
    frequency = int((1 / manager.user.frequency) * 60 * 60 * 1000)

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
    msg.set("You can go sleep (∪.∪ )...zzz\n we will take it from here 💪")

    def check_for_grades():
        # open page
        manager.browser.open("https://inbar.biu.ac.il/Live/Login.aspx")
        login_form = manager.browser.get_form()
        login_form['edtUsername'] = manager.user.username
        login_form['edtPassword'] = manager.user.password
        manager.browser.submit_form(login_form)

        today = datetime.date.today()
        page_html = manager.browser.parsed
        grade_block = page_html.find_all("div", {"id": "ContentPlaceHolder1_dvStudentGradesList"})
        for course_html in grade_block[0].find_all("tr"):
            name_str = course_html.find_all("td")[COURSE_NAME_HTML_INDEX].text
            date_str = course_html.find_all("td")[COURSE_DATE_HTML_INDEX].text
            grade_str = course_html.find_all("td")[COURSE_GRADE_HTML_INDEX].text
            if manager.user.courses_list.count(name_str) != 0:
                # TODAY minus the upload date of the new grade
                delta_time = today - convert_str_to_date(date_str)
                if int(delta_time.days) < MAX_DAYS_DELTA:
                    msg.set("A new grade uploaded: " + name_str + "\ngrade: " + grade_str)
                    return True
        return False

    def refresh():
        global refresh_count
        # refresh
        try:
            # checks for new grade
            if check_for_grades():
                manager.start_audio("win")
            else:
                refresh_count += 1
                count_str.set("Attempt count: " + str(refresh_count))
                manager.window.after(frequency, refresh)
        # in case there is no internet connection
        except exceptions.ConnectionError:
            pass
            # print("There is no internet connection. Try to connect automatically in "
            #       + str(INTERNET_CONNECTION_ERR_SLEEP_TIME) + " sec")
            # root3.after(int(INTERNET_CONNECTION_ERR_SLEEP_TIME * 1000), start_refresh)

    manager.window.after(0, refresh)
