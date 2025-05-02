from typing import Dict, Optional, Tuple
from domain.repository.reservation_repository import IReservationRepository
from domain.use_cases.reserve_book import Reserve_book

class DbReservation(IReservationRepository):
    def __init__(self):
        self.reservations: Dict[Tuple[int, int], Reserve_book] = {}

    def get_active_reservation(self, book_id: int, member_id: int) -> Optional[Reserve_book]:
        return self.reservations.get((book_id, member_id))

    def mark_as_returned(self, reservation_id: int) -> None:
        for reservation in self.reservations.values():
            if reservation.id == reservation_id:
                reservation.returned = True
                break

    def save(self, reservation: Reserve_book) -> None:
        self.reservations[(reservation.book_id, reservation.member_id)] = reservation