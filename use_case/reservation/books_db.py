


STATIC_BOOKS = [
    Book(1, "The Hobbit", "J.R.R. Tolkien", date(1937, 9, 21), True),
    Book(2, "1984", "George Orwell", date(1949, 6, 8), True),
    Book(3, "The Great Gatsby", "F. Scott Fitzgerald", date(1925, 4, 10), False)
]



class BookRepository(IBookRepository):
    def find_all(self) -> List[Book]:
        return STATIC_BOOKS.copy()  
    
    def find_by_id(self, book_id: int) -> Optional[Book]:
        return next((b for b in STATIC_BOOKS if b.id == book_id), None)
    
    def save(self, book: Book) -> None:
        existing = self.find_by_id(book.id)
        if existing:
            STATIC_BOOKS.remove(existing)
        STATIC_BOOKS.append(book)
    