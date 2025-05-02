from datetime import date
from domain.exceptions.book_exceptions.book_already_reserved import BookAlreadyReservedError
from model.entity_valueObject import Entity

class Book(Entity):

    def __init__(self , id : int , name : str , title : str , creation_date : date , available : bool) :
        self.id = id
        self.name = name
        self.title = title
        self.creation_date = creation_date
        self.available = available
    
    def reserve(self) -> None:
        if not self.available:
            raise BookAlreadyReservedError()
        self.available = False