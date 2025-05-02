from domain.model.reservation.reservation_duration import ReservationDuration
from domain.model.book.book import Book
from domain.model.member.member import Member
from domain.repository.book_repository import IBookRepository
from domain.repository.member_repository import IMemberRepository
from domain.repository.reservation_repository import IReservationRepository

class Reserve_book():
    def __init__(self, id: int, book: Book, member: Member, duration_days: ReservationDuration):
        self.id = id
        self.book = book
        self.book_id = book.id
        self.member = member
        self.member_id = member.id.id
        self.start_date = duration_days.start_date()
        self.duration_days = duration_days.days
        self.end_date = duration_days.end_date()
        self.returned = False

    def __str__(self):
        return (f"Reservation #{self.id}: {self.book.title} for {self.member.name} "
                f"from {self.start_date} to {self.end_date}")
    
    @staticmethod
    def create(id: int, book_id: int, member_id: int, duration: ReservationDuration,  book_repository: IBookRepository,
        member_repository: IMemberRepository) -> 'Reserve_book':
         
        member =  member_repository.get_by_id(member_id)
        book = book_repository.get_by_id(book_id)

        member.can_reserve()

        book.reserve()

        member_repository.save_member(member)
        book_repository.save(book)
            
        return Reserve_book(
                id=id,
                book=book,
                member=member,
                duration_days=duration
            )

