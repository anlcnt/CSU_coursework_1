from gui.treeviews.base import BaseTree
from db.models.lending import Lending


class LendingTree(BaseTree):
    def __init__(self, parent):
        headers = {
            "member_id": "Номер читательского билета",
            "member_name": "ФИО читателя",
            "book": "Книга",
            "lended_at": "Выдана",
            "returned_at": "Возвращена"
        }
        super().__init__(headers=headers, parent=parent)

        self.tag_configure("not_returned", background="lightgray")

    def push(self, lending: Lending):
        dt_f = "%d.%m.%Y %H:%M:%S"

        self.insert(parent="", index="end", iid=lending.id, values=[
            lending.member_id,
            lending.member.name,
            lending.book.name,
            lending.lended_at.strftime(dt_f),
            lending.returned_at.strftime(dt_f) if lending.returned_at else ""
        ], tag="returned" if lending.returned_at else "not_returned")
