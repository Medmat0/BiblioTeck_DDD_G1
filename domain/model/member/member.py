
from card import Card
from member.email import Email
from model.entity_valueObject import Entity


class Member(Entity):
    def __init__(self, id: Card, name: str, age: int, email: Email):
        self.id = id
        self.name = name
        self.age = age
        self.email = email