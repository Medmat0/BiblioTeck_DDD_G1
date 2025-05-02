from typing import List, Optional
from domain.repository.book_repository import IBookRepository
from domain.model.book.book import Book
from infrastructure.data.static_book import STATIC_BOOKS

class DbBook (IBookRepository):
    def __init__(self):
        self.books: List[Book] = STATIC_BOOKS.copy()
    
    def get_by_id(self, book_id: int) -> Optional[Book]:
        return next((book for book in self.books if book.id == book_id), None)
    
    def save(self, book: Book) -> None:
        existing_book = self.get_by_id(book.id)
        if existing_book:
            index = self.books.index(existing_book)
            self.books[index] = book
        else:
            self.books.append(book)
    
    def get_all_books(self) -> List[Book]:
        return self.books.copy()