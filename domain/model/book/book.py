from datetime import date
from model.entity_valueObject import Entity

class Book(Entity):

    def __init__(self , id : int , name : str , title : str , creation_date : date , available : bool) :
        self.id = id
        self.name = name
        self.title = title
        self.creation_date = creation_date
        self.available = available