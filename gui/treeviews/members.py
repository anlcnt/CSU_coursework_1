from gui.treeviews.base import BaseTree
from db.models.member import Member


class MembersTree(BaseTree):
    '''Таблица с читателями'''

    def __init__(self, parent):
        headers = {
            "name": "ФИО",
            "phone": "Телефон",
            "brith": "Дата рождения",
            "created_at": "Записан",
            "updated_at": "Обновлён"
        }
        super().__init__(headers=headers, parent=parent)

    def push(self, member: Member):
        self.insert(parent="", index="end", iid=member.id, values=[
            member.name,
            f"+7{member.phone}" if member.phone else "",  # Так, наверное, делать не стоит
            member.brith,
            member.created_at,
            member.updated_at
        ])
