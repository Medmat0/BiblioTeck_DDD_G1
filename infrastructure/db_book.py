from typing import List, Optional
from domain.model.book import Book
from domain.repository.book_repository import IBookRepository
from infrastructure.data.static_book import STATIC_BOOKS

class StaticBookRepository(IBookRepository):
    
    def __init__(self):
        self._books = STATIC_BOOKS.copy()  
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        return next((book for book in self._books if book.id == book_id), None)
    
    def get_all(self) -> List[Book]:
        return self._books.copy()
    
    def add(self, book: Book) -> None:
        if self.get_by_id(book.id) is None:
            self._books.append(book)
        else:
            raise ValueError(f"Book with ID {book.id} already exists")
    
    def update(self, id_book: int , available : bool) -> None:
        existing = self.get_by_id(id_book)
        if existing:
            existing.availabe = available
        else:
            raise ValueError(f"Book with ID {id_book} not found")
    
    def delete(self, book_id: int) -> bool:
        book = self.get_by_id(book_id)
        if book:
            self._books.remove(book)
            return True
        return False
    
    def get_available_books(self) -> List[Book]:
        return [book for book in self._books if book.available]