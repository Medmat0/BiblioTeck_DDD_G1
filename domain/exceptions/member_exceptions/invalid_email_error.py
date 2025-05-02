from exceptions.exceptions import DomainException

class InvalidEmailError(DomainException):
    def __init__(self, email):
        super().__init__(f"Invalid email address {email}")