from domain.exceptions.book_exceptions.book_already_reserved import BookAlreadyReservedError
from domain.exceptions.member_exceptions.card_expired import CardExpiredError
from domain.exceptions.member_exceptions.too_many_penalties import TooManyPenaltiesError
import pytest
from datetime import date, timedelta

from domain.exceptions.reservation_exceptions.invalid_reservation_duration import InvalidReservationDuration
from domain.model.book.book import Book
from domain.model.member.member import Member
from domain.model.member.card import Card
from domain.model.reservation.reservation_duration import ReservationDuration
from domain.repository.book_repository import IBookRepository
from domain.repository.member_repository import IMemberRepository
from domain.use_cases.reserve_book import Reserve_book
from infrastructure.db_book import DbBook
from infrastructure.db_member import DbMember


@pytest.fixture
def book_repo():
    return DbBook()  # Instantiate the class


@pytest.fixture
def member_repo():
    return DbMember()  # Instantiate the class


@pytest.fixture
def valid_duration():
    return ReservationDuration(14)


@pytest.fixture
def too_long_duration():
    return ReservationDuration(30)


class TestReservationSystem:
    def test_get_book_by_id(self, book_repo):
        book = book_repo.get_by_id(1)
        assert book is not None
        assert book.title == "Harry Potter and the Philosopher's Stone"
        assert book_repo.get_by_id(999) is None

    def test_get_member_by_id(self, member_repo):
        member = member_repo.get_by_id(1)
        assert member is not None
        assert member.name == "Benoit Suy"
        assert member_repo.get_by_id(999) is None

    def test_successful_reservation_creation(self, book_repo, member_repo, valid_duration):
        book = book_repo.get_by_id(1)
        member = member_repo.get_by_id(1)
        print(member.id.check_penality())

        reservation = Reserve_book.create(
            id=1,
            book_id=book.id,
            member_id=member.id.id,
            duration=valid_duration,
            book_repository=book_repo,
            member_repository=member_repo
        )

        assert reservation is not None
        assert reservation.book_id == book.id
        assert reservation.member_id == member.id.id
        assert reservation.end_date == date.today() + timedelta(days=14)

        updated_book = book_repo.get_by_id(book.id)
        assert updated_book.available is False

    def test_reserve_unavailable_book(self, book_repo, member_repo, valid_duration):
        with pytest.raises(BookAlreadyReservedError):  # Changez pour attraper la bonne exception
            Reserve_book.create(
                id=2,
                book_id=2,
                member_id=1,
                duration=valid_duration,
                book_repository=book_repo,
                member_repository=member_repo
            )

    def test_reserve_with_expired_card(self, book_repo, member_repo, valid_duration):
        
        with pytest.raises(CardExpiredError):
            Reserve_book.create(
                id=3,
                book_id=4,
                member_id=2,
                duration=valid_duration,
                book_repository=book_repo,
                member_repository=member_repo
            )

    def test_reserve_with_penalties(self, book_repo, member_repo, valid_duration):
        with pytest.raises(TooManyPenaltiesError):
            Reserve_book.create(
                id=4,
                book_id=5,
                member_id=3,
                duration=valid_duration,
                book_repository=book_repo,
                member_repository=member_repo
            )

    def test_reserve_with_too_long_duration(self, book_repo, member_repo):
        with pytest.raises(InvalidReservationDuration, match="Duration must be 1-30 days"):
            ReservationDuration(40)  # Test invalid duration directly

    def test_save_and_retrieve_updated_book(self, book_repo):
        book = book_repo.get_by_id(1)
        original_availability = book.available

        book.available = not original_availability
        book_repo.save(book)

        updated_book = book_repo.get_by_id(1)
        assert updated_book.available is not original_availability

    def test_save_and_retrieve_updated_member(self, member_repo):
        member = member_repo.get_by_id(1)
        original_name = member.name

        member.name = "Updated Name"
        member_repo.save_member(member)

        updated_member = member_repo.get_by_id(1)
        assert updated_member.name == "Updated Name"