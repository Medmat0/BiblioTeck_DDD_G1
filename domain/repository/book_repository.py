from abc import ABC, abstractmethod
from typing import List, Optional
from domain.model.book.book import Book

class IBookRepository(ABC):
    
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        pass
    
    @abstractmethod
    def save(self, book: Book) -> None: ...