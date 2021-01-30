class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.frequency = 60 * 6
        self.courses_list = []
