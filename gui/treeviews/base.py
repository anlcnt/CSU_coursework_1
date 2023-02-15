from tkinter.ttk import Treeview


class BaseTree(Treeview):
    '''Базовая таблица'''

    def __init__(self, headers: dict, parent):
        columns = tuple(headers.keys())
        super().__init__(parent, show="headings", columns=columns)

        for key in columns:
            self.heading(key, text=headers[key])

    def push(self, el):
        self.insert(parent="", index="end", iid=el.id, values=[el.name])

    def clear(self):
        self.delete(*self.get_children())

    def set_data(self, data):
        self.clear()

        for record in data:
            row = record[0]
            self.push(row)
