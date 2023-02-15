from gui.treeviews.base import BaseTree
from db.models.hall import Hall


class HallsTree(BaseTree):
    '''Таблица с читателями'''

    def __init__(self, parent):
        headers = {
            "name": "Зал",
            "name_field": "Область знаний"
        }
        super().__init__(headers=headers, parent=parent)

        self.tag_configure("field", background="lightgray")

    def push(self, hall: Hall):
        self.insert(parent="", index="end", iid=hall.id, values=[hall.name])
        for field in hall.fields:
            self.insert(parent="",
                        index="end",
                        iid=f"{hall.id}_{field.id}",
                        values=["", field.name],
                        tag="field")
