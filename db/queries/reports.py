''' Отчёты в соответствии с заданием '''

from sqlalchemy import select, func, extract

from db.models.member import Member
from db.models.lending import Lending
from db.models.book import Book
from db.models.hall import Hall
from db.models.field import Field


def books_by_year(member: Member, year: int):
    '''
        Посчитать за каждый месяц года,
        определенного пользователем, количество выдач книг
    '''
    month_extracted = extract('month', Lending.lended_at)
    year_extracted = extract('year', Lending.lended_at)

    query = select(month_extracted, func.count(Lending.book_id)
                   ).where(year_extracted == year
                           ).where(Lending.member_id == member.id
                                   ).group_by(month_extracted)

    return query


def oldest_books():
    '''
        Вывести название и возраст книги самой старой книги в каждом из залов.
    '''
    # TODO: Добавить залы
    query = select(Book, func.min(Book.year), Field
                   ).join(Field).join(Hall).group_by(Hall.id)

    return query


def best_books(month: int):
    '''
        Вывести 5 лучших книг, которые за прошедший месяц
        пользовались наибольшим спросом.
    '''
    month_extracted = extract('month', Lending.lended_at)

    query = select(Book, func.count(Book.id)
                   ).join(Lending
                          ).where(month_extracted == month
                                  ).group_by(Book.id).limit(5)

    return query


def get_hall_by_book_type():
    '''
        Вывести читальный зал в котором содержаться книги только заданных
        пользователем типов (типов при поиске может быть определено
        несколько). Условия поиска дополняется посредством where(),
        например: get_hall_by_book_type().where(Book.pages > 100)
    '''
    query = select(Hall).join(Field).join(Book)

    return query
