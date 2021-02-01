import tkinter as tk
import simpleaudio
from robobrowser import RoboBrowser


class Manager:
    def __init__(self):
        # Browser
        self.browser = RoboBrowser(history=False, parser="html.parser")
        self.refresh_thread = None
        # GUI - tkinter
        self.window = tk.Tk()
        self.window_bg = '#80c1ff'
        self.icon = tk.PhotoImage(file="./Photos/icon.png")
        self.window.iconphoto(False, self.icon)
        self.window.resizable(False, False)
        self.canvas = tk.Canvas(self.window, bg="PaleTurquoise1")
        self.canvas.pack()
        self.font = "Purisa"
        self.button_bg = "LightBlue2"
        # Audio
        self.audio = None
        # User
        self.user = None

    def init_window(self, width, height, title):
        self.window.title(title)
        self.canvas.config(width=width, height=height)

    def start_audio(self, name):
        path = 'Sounds/' + name + '.wav'
        wave_obj = simpleaudio.WaveObject.from_wave_file(path)
        self.audio = wave_obj.play()
