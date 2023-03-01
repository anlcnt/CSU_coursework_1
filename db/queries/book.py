''' Запросы по книгам '''

from sqlalchemy import select, or_, not_, func

from db.models.lending import Lending
from db.models.book import Book


def books_exists():
    '''
        Возвращает доступные книги для выдачи
    '''
    # query = select(Book).join(Lending).where(Lending.returned_at is not None or Lending.lended_at is None).group_by(Book.id)
    # query = select(Book).join(Lending).where(
    #     or_(func.length(Book.lendings) == 0, Lending.returned_at.isnot(None))).group_by(Book.id)
    # lending_query = select(Lending, func.max(Lending.lended_at)).group_by(Book.id)
    query = select([Book, func.max(Lending.lended_at)]).join(Lending, Book.id).where(or_(Lending.returned_at.isnot(None), Lending.lended_at.is_(None)))

    return query
