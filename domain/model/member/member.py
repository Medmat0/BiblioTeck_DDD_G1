
from domain.model.entity_valueObject import Entity
from domain.model.member.card import Card
from domain.model.member.email import Email


class Member(Entity):
    def __init__(self, id: Card, name: str, age: int, email: Email):
        self.id = id
        self.name = name
        self.age = age
        self.email = email