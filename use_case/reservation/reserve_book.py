from datetime import date, timedelta
from abc import ABC, abstractmethod

from domain.model.book.book import Book
from domain.model.member.member import Member
from domain.model.reservation.reservation import Reservation
from domain.model.member.card import Card
from domain.model.reservation.reservation_duration import ReservationDuration


# Interfaces
class IBookRepository(ABC):
    @abstractmethod
    def get_all_books(self) -> list: # pragma: no cover
        pass
    
    @abstractmethod
    def get_book_by_id(self, book_id: int): # pragma: no cover
        pass

class IMemberRepository(ABC):
    @abstractmethod
    def get_all_members(self) -> list: # pragma: no cover
        pass
    
    @abstractmethod
    def get_member_by_id(self, member_id: int): # pragma: no cover
        pass

class IReservation(ABC):
    @abstractmethod
    def reserve_book(self, book_id: int, member_id: int, duration_days: int): # pragma: no cover
        pass



# Repository Implementations
class BookRepository(IBookRepository):
    def __init__(self):
        self.books = []
    
    def get_all_books(self) -> list:
        return self.books
    
    def get_book_by_id(self, book_id: int):
        return next((b for b in self.books if b.id == book_id), None)
    
    def add_book(self, book: Book):
        self.books.append(book)
    
    def update_book_availability(self, book_id: int, available: bool):
        book = self.get_book_by_id(book_id)
        if book:
            book.available = available
            return True
        return False

class MemberRepository(IMemberRepository):
    def __init__(self):
        self.members = []
    
    def get_all_members(self) -> list:
        return self.members
    
    def get_member_by_id(self, member_id: int):
        return next((m for m in self.members if m.id.id == member_id), None)
     
    def add_member(self, member: Member):
        self.members.append(member)

# Reservation Service
class ReservationService(IReservation):
    MAX_PENALITIES = 5
    MAX_RESERVATION_DAYS = 30
    
    def __init__(self, book_repo: IBookRepository, member_repo: IMemberRepository):
        self.book_repo = book_repo
        self.member_repo = member_repo
        self.reservations = []

    def reserve_book(self, book_id: int, member_id: int, duration_days: int):
        if duration_days > self.MAX_RESERVATION_DAYS:
            raise ValueError(f"Maximum reservation duration is {self.MAX_RESERVATION_DAYS} days")
        if duration_days <= 0:
            raise ValueError("Reservation duration must be positive")

        member = self.member_repo.get_member_by_id(member_id)
        if not member:
            raise ValueError("Member not found")

        if member.id.check_penality() >= self.MAX_PENALITIES:
            raise ValueError(
                f"Member has {member.id.check_penality()} penalties (max allowed: {self.MAX_PENALITIES - 1})")

        if member.id.is_expired():
            raise ValueError(f"Member's card expired on {member.id.expiration_date}")

        book = self.book_repo.get_book_by_id(book_id)
        if not book:
            raise ValueError("Book not found")
        if not book.available:
            raise ValueError("Book is already reserved")

        # Create a ReservationDuration object
        duration = ReservationDuration(duration_days)

        reservation = Reservation(
            id=len(self.reservations) + 1,
            book=book,
            member=member,
            duration_days=duration  # Pass the ReservationDuration object
        )

        if not self.book_repo.update_book_availability(book_id, False):
            raise ValueError("Failed to update book status")

        self.reservations.append(reservation)
        return reservation


