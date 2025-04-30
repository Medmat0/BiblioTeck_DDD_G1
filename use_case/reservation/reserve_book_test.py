import pytest
from datetime import date, timedelta
from .reserve_book import (
    Book, Card, Member, 
    BookRepository, MemberRepository, 
    ReservationService, Reservation
)

@pytest.fixture
def setup():
    book_repo = BookRepository()
    member_repo = MemberRepository()
    
    # Setup members
    member_repo.add_member(Member(
        Card(1, date(2025, 12, 31), 0),
        "benoit", 30, "benoit@example.com"
    ))
    member_repo.add_member(Member(
        Card(2, date(2027, 12, 31), 8),
        "omar", 30, "omar@example.com"
    ))
    member_repo.add_member(Member(
        Card(3, date(2020, 12, 31), 0),
        "omar_benoit", 30, "omarbenoit@example.com"
    ))
    
    # Setup books
    book_repo.add_book(Book(101, "elmatror", "Blue Book", date(2019, 1, 1), True))
    book_repo.add_book(Book(102, "Yassine", "Red Book", date(2020, 1, 1), True))
    
    reservation_service = ReservationService(book_repo, member_repo)
    
    return {
        'book_repo': book_repo,
        'member_repo': member_repo,
        'service': reservation_service
    }

def test_valid_reservation(setup):
    reservation = setup['service'].reserve_book(101, 1, 14)
    assert reservation is not None
    assert reservation.book.id == 101
    assert reservation.member.id.id == 1
    assert reservation.duration_days == 14


def test_book_already_reserved(setup):
    setup['service'].reserve_book(101, 1, 14)
    with pytest.raises(ValueError, match="Book is already reserved"):
        setup['service'].reserve_book(101, 1, 14)



def test_member_with_penalties(setup):
    with pytest.raises(ValueError, match="Member has 8 penalties"):
        setup['service'].reserve_book(102, 2, 14)

def test_expired_card(setup):
    with pytest.raises(ValueError, match="Member's card expired on"):
        setup['service'].reserve_book(102, 3, 14)

def test_too_long_duration(setup):
    with pytest.raises(ValueError, match="Maximum reservation duration is 30 days"):
        setup['service'].reserve_book(102, 1, 60)

def test_non_existent_book(setup):
    with pytest.raises(ValueError, match="Book not found"):
        setup['service'].reserve_book(999, 1, 14)

def test_non_existent_member(setup):
    with pytest.raises(ValueError, match="Member not found"):
        setup['service'].reserve_book(101, 999, 14)