from datetime import date
from member.card import Card
from member.member import Member


STATIC_MEMBERS = [
    Member(
        id=1,
        card=Card(
            id=1,
            expiration_date=date(2025, 12, 31),
            penalty_count=0
        ),
        name="Benoit Suy",
        age=23,
        email="benoit.suy@gmail.com"
    ),
    Member(
        id=2,
        card=Card(
            id=2,
            expiration_date=date(2025, 6, 30),  # Expired card
            penalty_count=0
        ),
        name="ELMATROR Yassine",
        age=23,
        email="elmatror.yassine@gmail.com"
    ),
    Member(
        id=3,
        card=Card(
            id=3,
            expiration_date=date(2028, 12, 31),
            penalty_count=3  
        ),
        name="Omar EL BARAKA",
        age=25,
        email="elbaraka.omar@gmail.com"
    )
]