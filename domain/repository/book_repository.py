from abc import ABC, abstractmethod
from typing import List, Optional
from domain.model.book.book import Book

class IBookRepository(ABC):
    
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Book]:
        pass
    
    @abstractmethod
    def add(self, book: Book) -> None:
        pass
    
    @abstractmethod
    def update_available(self, id_book: int , available : bool) -> None:
        pass
    
    @abstractmethod
    def delete(self, book_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_available_books(self) -> List[Book]:
        pass