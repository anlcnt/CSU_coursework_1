from gui.treeviews.base import BaseTree
from db.models.field import Field


class FieldsTree(BaseTree):
    '''Таблица с областями знаний'''

    def __init__(self, parent):
        headers = {
            "name": "Область знаний",
            "name_hall": "Зал",
            "book_count": "Кол-во книг"
        }
        super().__init__(headers=headers, parent=parent)

        self.tag_configure("empty", background="yellow")

    def push(self, field: Field):
        books_count = len(field.books)
        self.insert(parent="", index="end", iid=field.id, values=[
            field.name,
            field.hall.name,
            books_count
        ], tag=("empty" if not books_count else "not_empty"))
