
from domain.exceptions.member_exceptions.card_expired import CardExpiredError
from domain.exceptions.member_exceptions.too_many_penalties import TooManyPenaltiesError
from domain.model.member.card import Card
from domain.model.member.email import Email
from domain.model.names_DDD import Entity


class Member(Entity):
    def __init__(self, id: Card, name: str, age: int, email: Email):
        self.id = id
        self.name = name
        self.age = age
        self.email = email

    def can_reserve(self) -> None:
        if self.id.is_expired():
            raise CardExpiredError(self.id.expiration_date)
        if self.id.check_penality() :
            raise TooManyPenaltiesError(5)