class UserIsNotAdminException(Exception):
    def __init__(self, message="User is not admin"):
        self.message = message
        super().__init__(self.message)


class DeviceNotFound(Exception):
    def __init__(self, message="Device not found"):
        self.message = message
        super().__init__(self.message)


class DeviceLocationNotFound(Exception):
    def __init__(self, message="Device location not found"):
        self.message = message
        super().__init__(self.message)