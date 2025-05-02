
from datetime import date, timedelta

from domain.model.entity_valueObject import Entity


class Card (Entity):
    def __init__(self, id: int, expiration_date: date, penality_count: int):
        self.id = id
        self.penality_count = penality_count
        self.expiration_date = expiration_date
        self.MAX_PENALTIES = 5

    def check_penality(self):
        return self.penality_count >= self.MAX_PENALTIES
    
    def is_expired(self):
        return self.expiration_date < date.today()