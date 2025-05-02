from exceptions.exceptions import DomainException



class BookNotFoundError(DomainException):
    pass

class BookAlreadyReservedError(DomainException):
    pass