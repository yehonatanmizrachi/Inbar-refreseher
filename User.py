class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.frequency = 60  # per hour
        self.courses_list = []
