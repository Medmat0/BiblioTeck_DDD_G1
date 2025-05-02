from datetime import date

from domain.model.member.card import Card
from domain.model.member.email import Email
from domain.model.member.member import Member

STATIC_MEMBERS = [
    Member(
        id=Card(
            id=1,
            expiration_date=date(2025, 12, 31),
            penality_count=0
        ),
        name="Benoit Suy",
        age=23,
        email=Email("benoit.suy@gmail.com")
    ),
    Member(
        id=Card(
            id=2,
            expiration_date=date(2025, 6, 30),  # Expired card
            penality_count=0
        ),
        name="ELMATROR Yassine",
        age=23,
        email=Email("elmatror.yassine@gmail.com")
    ),
    Member(
        id=Card(
            id=3,
            expiration_date=date(2028, 12, 31),
            penality_count=3
        ),
        name="Omar EL BARAKA",
        age=25,
        email=Email("elbaraka.omar@gmail.com")
    )
]