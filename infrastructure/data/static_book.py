from datetime import date
from domain.model.book.book import Book

STATIC_BOOKS = [
    Book(
        id=1,
        name="J.K. Rowling",
        title="Harry Potter and the Philosopher's Stone",
        creation_date=date(1997, 6, 26),
        available=True
    ),
    Book(
        id=2,
        name="George Orwell",
        title="1984",
        creation_date=date(1949, 6, 8),
        available=False
    ),
    Book(
        id=3,
        name="J.R.R. Tolkien",
        title="The Hobbit",
        creation_date=date(1937, 9, 21),
        available=True
    ) ,
        Book(
        id=4,
        name="Red book",
        title="DDD",
        creation_date=date(1997, 6, 26),
        available=True
    ),

       Book(
        id=5,
        name="Clean code",
        title=" How to clean your code",
        creation_date=date(1997, 6, 26),
        available=True
    )
]