from datetime import timedelta
from domain.model.reservation.reservation_duration import ReservationDuration
from infrastructure.db_member import DbMember
from infrastructure.db_book import DbBook
from domain.use_cases.reserve_book import Reserve_book

def main():
    # Initialisation des repositories
    member_repository = DbMember()
    book_repository = DbBook()

    # Choix d'un livre et d'un membre valides (ex : livre 1 et membre 1)
    book_id = 1
    member_id = 1
    reservation_id = 101
    duration_days = 14  # entre 1 et 30

    # Créer la durée de réservation
    class Duration(ReservationDuration):
        def __init__(self, days):
            self.days = days
            self.__post_init__()

    try:
        duration = Duration(duration_days)
        reservation = Reserve_book.create(
            id=reservation_id,
            book_id=book_id,
            member_id=member_id,
            duration=duration,
            book_repository=book_repository,
            member_repository=member_repository
        )
        print(reservation)
    except Exception as e:
        print(f"Erreur lors de la réservation : {e}")

if __name__ == "__main__":
    main()
