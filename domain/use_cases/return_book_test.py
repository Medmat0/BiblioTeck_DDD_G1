import pytest
from datetime import date, timedelta
from domain.model.book.book import Book
from domain.model.member.card import Card
from domain.model.member.member import Member
from domain.model.member.email import Email
from domain.repository.book_repository import IBookRepository
from domain.repository.member_repository import IMemberRepository
from domain.repository.reservation_repository import IReservationRepository
from domain.model.reservation.reservation_duration import ReservationDuration
from domain.use_cases.reserve_book import Reserve_book as Reservation
from .return_book import ReturnBookService, IPenaltyService

class FakeBookRepository(IBookRepository):
    def __init__(self):
        today = date.today()
        self.books = {
            1: Book(1, "Dune", "Dune", today, False),
            2: Book(2, "1984", "1984", today, False),
            3: Book(3, "Le Petit Prince", "Le Petit Prince", today, False)
        }
    
    def get_by_id(self, book_id): 
        return self.books.get(book_id)
    
    def save(self, book): 
        self.books[book.id] = book

class FakeMemberRepository(IMemberRepository):
    def __init__(self):
        self.members = {
            1: Member(Card(1, date(2026, 1, 1), 0), "Omar", 25, Email("omar@example.com")),
            2: Member(Card(2, date(2030, 1, 1), 0), "Yassine", 30, Email("yassine@example.com")),
            3: Member(Card(3, date(2020, 1, 1), 0), "Benoit", 35, Email("benoit@example.com"))  
        }
    
    def get_by_id(self, member_id): 
        return self.members.get(member_id)
    
    def save_member(self, member): 
        self.members[member.id] = member

class FakeReservationRepository(IReservationRepository):
    def __init__(self):
        self.reservations = {}
        today = date.today()
        # créée il y a 10 jours avec une durée de 5 jours
        omar_reservation = Reservation(
            1, 
            Book(1, "Dune", "Dune", today, False),
            Member(Card(1, date(2030, 1, 1), 0), "Omar", 25, Email("omar@example.com")),
            ReservationDuration(5)
        )
        omar_reservation.start_date = today - timedelta(days=10)
        omar_reservation.end_date = today - timedelta(days=5)
        self.reservations[(1, 1)] = omar_reservation

        self.reservations[(2, 2)] = Reservation(
            2,
            Book(2, "1984", "1984", today, False),
            Member(Card(2, date(2030, 1, 1), 0), "Yassine", 30, Email("yassine@example.com")),
            ReservationDuration(10)
        )

        benoit_reservation = Reservation(
            3,
            Book(3, "Le Petit Prince", "Le Petit Prince", today, False),
            Member(Card(3, date(2020, 1, 1), 0), "Benoit", 35, Email("benoit@example.com")),
            ReservationDuration(5)
        )
        benoit_reservation.returned = True
        self.reservations[(3, 3)] = benoit_reservation

    def get_active_reservation(self, book_id, member_id):
        return self.reservations.get((book_id, member_id))

    def mark_as_returned(self, reservation_id):
        for key, res in self.reservations.items():
            if res.id == reservation_id:
                res.returned = True

    def save(self, reservation):
        self.reservations[(reservation.book_id, reservation.member_id)] = reservation

class FakePenaltyService(IPenaltyService):
    def __init__(self): self.penalties = {}
    def apply_penalty(self, member_id, days_late): self.penalties[member_id] = days_late


def test_return_book_late_omar():
    book_repo = FakeBookRepository()
    member_repo = FakeMemberRepository()
    res_repo = FakeReservationRepository()
    penalty_service = FakePenaltyService()
    service = ReturnBookService(book_repo, member_repo, res_repo, penalty_service)

    result = service.return_book(1, 1)

    assert res_repo.get_active_reservation(1, 1).returned is True
    assert penalty_service.penalties[1] == 5
    assert result == "Book 'Dune' returned by Omar"

def test_return_book_on_time_yassine():
    book_repo = FakeBookRepository()
    member_repo = FakeMemberRepository()
    res_repo = FakeReservationRepository()
    penalty_service = FakePenaltyService()
    service = ReturnBookService(book_repo, member_repo, res_repo, penalty_service)

    result = service.return_book(2, 2)

    assert res_repo.get_active_reservation(2, 2).returned is True
    assert 2 not in penalty_service.penalties
    assert result == "Book '1984' returned by Yassine"

def test_return_book_already_returned_benoit():
    book_repo = FakeBookRepository()
    member_repo = FakeMemberRepository()
    res_repo = FakeReservationRepository()
    penalty_service = FakePenaltyService()
    service = ReturnBookService(book_repo, member_repo, res_repo, penalty_service)

    with pytest.raises(ValueError, match="Book already returned"):
        service.return_book(3, 3)

def test_return_book_member_not_found():
    book_repo = FakeBookRepository()
    member_repo = FakeMemberRepository()
    res_repo = FakeReservationRepository()
    penalty_service = FakePenaltyService()
    service = ReturnBookService(book_repo, member_repo, res_repo, penalty_service)

    with pytest.raises(ValueError, match="Member not found"):
        service.return_book(1, 999)

def test_return_book_no_reservation():
    book_repo = FakeBookRepository()
    member_repo = FakeMemberRepository()
    res_repo = FakeReservationRepository()
    penalty_service = FakePenaltyService()
    service = ReturnBookService(book_repo, member_repo, res_repo, penalty_service)

    with pytest.raises(ValueError, match="No active reservation found"):
        service.return_book(3, 1)

def test_return_book_book_not_found():
    book_repo = FakeBookRepository()
    member_repo = FakeMemberRepository()
    res_repo = FakeReservationRepository()
    penalty_service = FakePenaltyService()
    service = ReturnBookService(book_repo, member_repo, res_repo, penalty_service)

    with pytest.raises(ValueError, match="Book not found"):
        service.return_book(999, 1)
