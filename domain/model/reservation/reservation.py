from book.book import Book
from model.entity_valueObject import Entity
from member.member import Member
from datetime import date, timedelta
from reservation.reservation_duration import ReservationDuration

class Reservation(Entity):
    def __init__(self, id: int, book: Book, member: Member, duration_days:ReservationDuration ):
        self.id = id
        self.book = book
        self.member = member
        self.start_date = duration_days.start_date()
        self.duration_days = duration_days
        self.end_date = duration_days.end_date()
        self.returned = False

    def __str__(self):
        return (f"Reservation #{self.id}: {self.book.title} for {self.member.name} "
                f"from {self.start_date} to {self.end_date}")
    
    @staticmethod
    def create(id: int, book: Book, member: Member, duration: ReservationDuration) -> 'Reservation':
        
        member.can_reserve()

        book.reserve()
            
        return Reservation(
                id=id,
                book=book,
                member=member,
                duration_days=duration
            )
            
       