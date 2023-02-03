from tkinter.ttk import Treeview

from db.models.member import Member


class LendingView(Treeview):
    def __init__(self, parent):
        headers = {
            "member_id": "Номер читательского билета",
            "member_name": "ФИО читателя",
            "book": "Книга",
            "lended_at": "Выдана",
            "returned_at": "Возвращена"
        }
        columns = tuple(headers.keys())
        super().__init__(parent, show="headings", columns=columns)

        for key in columns:
            self.heading(key, text=headers[key])

    def _columns(self):
        return [column.key for column in Member.__table__.columns]

    def push(self, lending):
        self.insert(index="end", text=f"{lending.id}", values=[
            lending.member_id,
            lending.member.name,
            lending.book.name,
            lending.lended_at,
            lending.returned_at
        ])
