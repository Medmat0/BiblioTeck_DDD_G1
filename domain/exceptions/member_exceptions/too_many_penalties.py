from domain.exceptions.exceptions import DomainException

class TooManyPenaltiesError(DomainException):
    def __init__(self, max_penalties):
        self.max_penalties = max_penalties