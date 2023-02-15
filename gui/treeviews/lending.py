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
        
        self.tag_configure("not_returned", background="yellow")

    def push(self, lending: Lending):
        self.insert(parent="", index="end", text=f"{lending.id}", values=[
            lending.member_id,
            lending.member.name,
            lending.book.name,
            lending.lended_at,
            lending.returned_at or "Не возвращена"
        ], tag="not_returned" if lending.returned_at is None else "")
