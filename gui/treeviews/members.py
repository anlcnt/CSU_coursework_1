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
        dt_f = "%d.%m.%Y %H:%M:%S"

        self.insert(parent="", index="end", iid=member.id, values=[
            member.name,
            f"+7{member.phone}" if member.phone else "",
            member.brith.strftime("%d.%m.%Y"),
            member.created_at.strftime(dt_f),
            member.updated_at.strftime(dt_f)
        ])
