from datetime import date
from abc import ABC, abstractmethod

from domain.model.book.book import Book
from domain.model.member.member import Member
from domain.model.member.card import Card
from domain.model.member.email import Email
from domain.model.reservation.reservation_duration import ReservationDuration
from domain.repository.book_repository import IBookRepository
from domain.repository.member_repository import IMemberRepository
from domain.repository.reservation_repository import IReservationRepository
from domain.use_cases.reserve_book import Reserve_book

class IPenaltyService(ABC):
    @abstractmethod
    def apply_penalty(self, member_id: int, days_late: int) -> None: pass

class ReturnBookService:
    def __init__(self, book_repo: IBookRepository,
                 member_repo: IMemberRepository,
                 reservation_repo: IReservationRepository,
                 penalty_service: IPenaltyService):
        self.book_repo = book_repo
        self.member_repo = member_repo
        self.reservation_repo = reservation_repo
        self.penalty_service = penalty_service

    def return_book(self, book_id: int, member_id: int) -> str:
        member: Member = self.member_repo.get_by_id(member_id)
        if not member:
            raise ValueError("Member not found")

        book: Book = self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found")

        reservation: Reserve_book = self.reservation_repo.get_active_reservation(book_id, member_id)
        if not reservation:
            raise ValueError("No active reservation found")

        if reservation.returned:
            raise ValueError("Book already returned")

        today = date.today()
        if today > reservation.end_date:
            days_late = (today - reservation.end_date).days
            self.penalty_service.apply_penalty(member_id, days_late)

        self.reservation_repo.mark_as_returned(reservation.id)
        book.make_available()
        self.book_repo.save(book)

        return f"Book '{book.title}' returned by {member.name}"

