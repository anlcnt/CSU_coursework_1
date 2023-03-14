from gui.treeviews.base import BaseTree
from db.models.book import Book


class BooksTree(BaseTree):
    '''Таблица с читателями'''

    def __init__(self, parent):
        headers = {
            "name": "Наименование",
            "author": "Автор",
            "publisher": "Издатель",
            "year": "Год издания",
            "place": "Город",
            "pages": "Кол-во страниц",
            "fiels": "Область знаний",
            "hall": "Зал",
        }
        super().__init__(headers=headers, parent=parent)

    def push(self, book: Book):
        self.insert(parent="", index="end", iid=book.id, values=[
            book.name,
            book.author.name,
            book.publisher.name,
            book.year,
            book.publisher.place,
            book.pages,
            book.field.name,
            book.field.hall.name
        ])
