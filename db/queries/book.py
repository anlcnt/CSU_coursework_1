from sqlalchemy import select

from db.models.lending import Lending
from db.models.book import Book


def get_books(session, order_by=Book.id):
    query = select(Book).order_by(order_by)
    return session.execute(query).all()


# Проверка наличии книги
# TODO: переделать
def book_exists(session, book):
    return session.query(Lending) \
        .filter(Lending.book_id == book.id) \
        .filter(exists().where(Lending.returned_at is None)).scalar()
