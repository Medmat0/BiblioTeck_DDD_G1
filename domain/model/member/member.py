from card import Card
from domain.exceptions.member_exceptions.card_expired import CardExpiredError
from domain.exceptions.member_exceptions.too_many_penalties import TooManyPenaltiesError
from member.email import Email
from model.entity_valueObject import Entity


class Member(Entity):
    def __init__(self, id: Card, name: str, age: int, email: Email):
        self.id = id
        self.name = name
        self.age = age
        self.email = email

    def can_reserve(self) -> None:
        if self.id.is_expired():
            raise CardExpiredError(self.id.expiration_date)
        if self.id.check_penality :
            raise TooManyPenaltiesError(Card.MAX_PENALTIES)