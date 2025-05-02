from dataclasses import dataclass
from exceptions.member_exceptions.invalid_email_error import InvalidEmailError
from names_DDD import ValueObject


class Email(ValueObject):
    def __init__(self, address: str):
        if not self._is_valid(address):
            raise InvalidEmailError(address)
        self.address = address
    
    def _is_valid(self, email: str) -> bool:
        return "@" in email and "." in email.split("@")[-1]
    
    def __eq__(self, other):
        if not isinstance(other, Email):
            return False
        return self.address == other.address
    
    def __str__(self):
        return self.address