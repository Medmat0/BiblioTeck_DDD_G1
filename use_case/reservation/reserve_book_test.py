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

def test_reservation_fails_when_card_expired():
    from datetime import date, timedelta

    book_repo = BookRepository()
    member_repo = MemberRepository()
    service = ReservationService(book_repo, member_repo)

    expired_card = Card(id=1, expiration_date=date.today() - timedelta(days=1), penality_count=0)
    member = Member(id=expired_card, name="Jean", age=30, email="jean@example.com")
    book = Book(id=1, name="123", title="Test Book", creation_date=date.today(), available=True)

    member_repo.add_member(member)
    book_repo.add_book(book)

    with pytest.raises(ValueError, match="expired"):
        service.reserve_book(book_id=1, member_id=1, duration_days=5)


def test_reservation_str():
    from datetime import date

    book = Book(id=1, name="abc", title="My Book", creation_date=date.today(), available=True)
    card = Card(id=1, expiration_date=date.today() + timedelta(days=10), penality_count=0)
    member = Member(id=card, name="Alice", age=25, email="alice@example.com")

    reservation = Reservation(id=1, book=book, member=member, duration_days=7)
    description = str(reservation)

    assert "Reservation #1" in description
    assert "My Book" in description
    assert "Alice" in description

def test_update_book_availability_fails(setup):
    setup['book_repo'].update_book_availability = lambda book_id, available: False
    with pytest.raises(ValueError, match="Failed to update book status"):
        setup['service'].reserve_book(101, 1, 14)

def test_reservation_with_zero_duration(setup):
    with pytest.raises(ValueError, match="Reservation duration must be positive"):
        setup['service'].reserve_book(101, 1, 0)

def test_reservation_returned_object(setup):
    reservation = setup['service'].reserve_book(101, 1, 14)
    assert isinstance(reservation, Reservation)
    assert reservation.book.id == 101
    assert reservation.member.id.id == 1
    assert reservation.duration_days == 14


def test_get_all_books():
    book_repo = BookRepository()
    book1 = Book(1, "Author1", "Title1", date(2020, 1, 1), True)
    book2 = Book(2, "Author2", "Title2", date(2021, 1, 1), True)

    book_repo.add_book(book1)
    book_repo.add_book(book2)
    all_books = book_repo.get_all_books()

    assert len(all_books) == 2
    assert book1 in all_books
    assert book2 in all_books

def test_update_book_availability_returns_false():
    book_repo = BookRepository()
    non_existent_book_id = 999

    result = book_repo.update_book_availability(non_existent_book_id, False)

    assert result is False

def test_get_all_members():
    member_repo = MemberRepository()
    member1 = Member(Card(1, date(2025, 12, 31), 0), "Alice", 25, "alice@example.com")
    member2 = Member(Card(2, date(2026, 12, 31), 1), "Bob", 30, "bob@example.com")

    member_repo.add_member(member1)
    member_repo.add_member(member2)
    all_members = member_repo.get_all_members()

    assert len(all_members) == 2
    assert member1 in all_members
    assert member2 in all_members