# pyinstaller --onefile --windowed --icon=Photos/icon.ico Index.py
from Manager import Manager
from Login import start_login

manager = Manager()
start_login(manager)
