from domain.exceptions.exceptions import DomainException


class TooManyPenaltiesError(DomainException):
    def __init__(self, max_penalties):
        super().__init__(f"Max penalties exceeded (max: {max_penalties})")