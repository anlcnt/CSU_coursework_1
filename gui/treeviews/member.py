from tkinter.ttk import Treeview

from db.models.member import Member


class MembersView(Treeview):
    def __init__(self, parent):
        headers = {
            "name": "ФИО",
            "phone": "Телефон",
            "brith": "Дата рождения",
            "created_at": "Записан",
            "updated_at": "Обновлён"
        }
        columns = tuple(headers.keys())
        super().__init__(parent, show="headings", columns=columns)

        for key in columns:
            self.heading(key, text=headers[key])

    def _columns(self):
        return [column.key for column in Member.__table__.columns]

    def push(self, member):
        self.insert(index="end", text=f"Билет №{member.id}", values=[
            member.name,
            member.phone,
            member.brith,
            member.created_at,
            member.updated_at
        ])
