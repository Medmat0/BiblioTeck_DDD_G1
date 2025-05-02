class DomainException(Exception):
    pass

class InvalidReservationDuration(DomainException):
    pass



class TooManyPenaltiesError(DomainException):
    def __init__(self, max_penalties):
        super().__init__(f"Max penalties exceeded (max: {max_penalties})")

class CardExpiredError(DomainException):
    pass

class BookNotFoundError(DomainException):
    pass

class BookAlreadyReservedError(DomainException):
    pass

class InvalidEmailError(DomainException):
    def __init__(self, email):
        super().__init__(f"Invalid email address {email}")