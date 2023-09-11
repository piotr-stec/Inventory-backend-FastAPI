class UserIsNotAdminException(Exception):
    def __init__(self, message="User is not admin"):
        self.message = message
        super().__init__(self.message)


class EmailAlreadyExists(Exception):
    def __init__(self, message="Email already exists"):
        self.message = message
        super().__init__(self.message)


class UserNameAlreadyExists(Exception):
    def __init__(self, message="Username already exists"):
        self.message = message
        super().__init__(self.message)


class UserNotFound(Exception):
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)


class DeviceNotFound(Exception):
    def __init__(self, message="Device not found"):
        self.message = message
        super().__init__(self.message)


class DeviceIsLoaned(Exception):
    def __init__(self, message="Device is loaned"):
        self.message = message
        super().__init__(self.message)


class LoanedDeviceOrEmpNotFound(Exception):
    def __init__(self, message="Loaned device or emp not found"):
        self.message = message
        super().__init__(self.message)


class DeleteDenied(Exception):
    def __init__(self, message="Delete denied: can not delete your own account"):
        self.message = message
        super().__init__(self.message)