
from dataclasses import dataclass
from datetime import timedelta, date
from domain.exceptions.reservation_exceptions.invalid_reservation_duration import InvalidReservationDuration
from domain.model.names_DDD import DomainService


class ReservationDuration(DomainService):
    MAX_DAYS = 30

    def __init__(self, days:int):
        self.days=days

        if not 1 <= self.days <= self.MAX_DAYS:
            raise InvalidReservationDuration(f"Duration must be 1-{self.MAX_DAYS} days")
    def __post_init__(self , days:int):
        self.days = days
        if not 1 <= self.days <= self.MAX_DAYS:
            raise InvalidReservationDuration(f"Duration must be 1-{self.MAX_DAYS} days")
    
    def start_date(self) -> date : 
        return date.today()

    def end_date(self) -> date:
        return date.today() + timedelta(days=self.days)