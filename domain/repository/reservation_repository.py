from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

class IReservationRepository(ABC):
    @abstractmethod
    def get_active_reservation(self, book_id: int, member_id: int) -> "Reserve_book":
        """Get the active reservation for a book and member"""
        pass

    @abstractmethod
    def mark_as_returned(self, reservation_id: int) -> None:
        """Mark a reservation as returned"""
        pass

    @abstractmethod
    def save(self, reservation: "Reserve_book") -> None:
        """Save a reservation"""
        pass