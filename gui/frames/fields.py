import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from datetime import datetime
from sqlalchemy import select, insert, update, delete
from db.models.field import Field
from db.models.hall import Hall
from gui.treeviews.fields import FieldsTree
from gui.frames.base import BaseView, BaseControl, BaseInputFrame as BIF, error_catcher


class FieldInputFrame(BIF):
    ''' Фрейм ввода области знаний '''

    def __init__(self, master, session, handler=None, selected_id=None):
        labels = ["Наименование", "Зал"]

        super().__init__(master, session, labels, handler, selected_id)

        self.halls = self.get_rows(Hall)

        self.name_entry = ttk.Entry(self, width=40)
        self.hall_combobox = ttk.Combobox(
            self, width=37, values=list(self.halls.keys()))

        BIF.set_grid(self.name_entry, 0)
        BIF.set_grid(self.hall_combobox, 1)
        BIF.set_grid(self.accept_button, 2)

    def hall_id(self):
        hall = self.hall_combobox.get()

        if hall in self.halls.keys():
            return self.halls[self.hall_combobox.get()]

        if askyesno(message="Указанный зал отсутствует. Создать?"):
            self.create_new_record(Hall, name=hall)
            return len(self.halls) + 1

        raise ValueError("Указанный зал отсутствует в базе")

    def get_data(self):
        return {
            "name": self.name_entry.get(),
            "hall_id": self.hall_id(),
            "updated_at": datetime.now()
        }


class FieldView(BaseView):
    '''Фрейм областей знаний'''

    def __init__(self, master, session):
        super().__init__(master, session)

        # Управление
        self.control = BaseControl(self)

        # Таблица
        self.treeview = FieldsTree(self)
        ysb = ttk.Scrollbar(self,
                            orient=tk.VERTICAL,
                            command=self.treeview.yview)

        self.treeview.configure(yscroll=ysb.set)

        # Обновление данных когда фрейм видимый
        self.bind("<Visibility>", self.update_treeview_data)

        self.control.pack()
        self.treeview.pack(expand=True)

    # Обновление данных
    def update_treeview_data(self, event=None):
        query = select(Field)
        result = self.session.execute(query).all()
        self.treeview.set_data(result)

    # Вызов окна добавления
    def add_data_command(self):
        FieldInputFrame(tk.Toplevel(),
                        self.session, self.add_data_handler).pack()

    # Вызов окна поиска
    def search_data_command(self):
        FieldInputFrame(tk.Toplevel(),
                        self.session, self.search_data_handler).pack()

    # Вызов окна редактирования
    def edit_data_command(self):
        iid, values = self.selected()
        frame = FieldInputFrame(tk.Toplevel(),
                                self.session,
                                self.edit_data_handler, iid)

        frame.name_entry.insert(0, values[0])
        frame.hall_combobox.insert(0, values[1])
        frame.pack()

    # Команда на удаление
    @error_catcher
    def remove_data_command(self):
        query = delete(Field).where(Field.id == self.treeview.focus())
        self.session.execute(query)

    # Обработка добавления
    @error_catcher
    def add_data_handler(self, frame, *args, **kwargs):
        self.session.execute(insert(Field), [frame.get_data()])

    # Обработка поиска
    @error_catcher
    def search_data_handler(self, frame, *args, **kwargs):
        query = select(Field)

        name = frame.name_entry.get()
        hall = frame.hall_combobox.get()

        conditions = [
            (name, Field.name == name),
            (hall, Field.hall == frame.hall_id())
        ]

        for c in conditions:
            if c[0]:
                query.where(c[1])

        result = self.session.execute(query).all()
        self.treeview.set_data(result)

    # Обработка редактирования
    @error_catcher
    def edit_data_handler(self, frame, selected_id, *args, **kwargs):
        query = update(Field).where(Field.id == selected_id)
        query = query.values({
            **frame.get_data(),
            "updated_at": datetime.now()
        })
        self.session.execute(query)
