


class UserExistsException(Exception):

    def __init__(self, username: str):
        self.username = username
        super().__init__(f"Username {self.username} already exists")