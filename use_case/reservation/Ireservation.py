from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional

class IBookRepository(ABC):
    """Interface defining all book-related operations."""
    
    @abstractmethod
    def get_all_books(self) -> List['Book']:
        """Get all books."""
        pass
    
    @abstractmethod
    def get_book_by_id(self, book_id: int) -> Optional['Book']:
        """Get a book by ID (returns None if not found)."""
        pass
    
    @abstractmethod
    def add_book(self, book: 'Book') -> None:
        """Add a new book."""
        pass
    
    @abstractmethod
    def update_book(self, book: 'Book') -> None:
        """Update an existing book."""
        pass
    
    @abstractmethod
    def delete_book(self, book_id: int) -> bool:
        """Delete a book by ID. Returns True if deleted, False if not found."""
        pass
    
    @abstractmethod
    def get_available_books(self) -> List['Book']:
        """Get all available books (where available=True)."""
        pass