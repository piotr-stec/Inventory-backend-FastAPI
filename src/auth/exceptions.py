class InvalidCredentialsException(Exception):
    def __init__(self, message="Invalid credentials"):
        self.message = message
        super().__init__(self.message)


class InactiveUserException(Exception):
    def __init__(self, message="Inactive user"):
        self.message = message
        super().__init__(self.message)