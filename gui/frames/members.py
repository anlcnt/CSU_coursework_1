import tkinter as tk
from tkinter import ttk
from datetime import datetime
from sqlalchemy import select, update, insert, delete
from db.models.member import Member
from gui.treeviews.members import MembersTree
from gui.frames.base import BaseView, BaseControl, BaseInputFrame as BIF, error_catcher


class MemberInputFrame(BIF):
    ''' Фрейм ввода читателей '''

    def __init__(self, master, session, handler=None, selected_id=None):
        labels = ["ФИО", "Дата рождения", "Телефон"]

        super().__init__(master, session, labels, handler, selected_id)

        self.name_entry = ttk.Entry(self, width=40)
        self.brith_entry = ttk.Entry(self, width=40)
        self.phone_entry = ttk.Entry(self, width=40)

        BIF.set_grid(self.name_entry, 0)
        BIF.set_grid(self.brith_entry, 1)
        BIF.set_grid(self.phone_entry, 2)
        BIF.set_grid(self.accept_button, 3)

    def name(self):
        return self.name_entry.get()

    def brith(self):
        value = self.brith_entry.get()
        if value:
            try:
                return datetime.strptime(value, "%d.%m.%Y")
            except ValueError:
                raise("Неверный формат даты")
        return None

    def phone(self):
        return self.phone_entry.get()

    def get_data(self):
        return {
            "name": self.name(),
            "brith": self.brith(),
            "phone": self.phone(),
        }


class MembersView(BaseView):
    '''Фрейм читателей'''

    def __init__(self, master, session):
        super().__init__(master, session)

        # Управление
        self.control = BaseControl(self)

        # Таблица
        self.treeview = MembersTree(self)
        ysb = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.treeview.yview)
        self.treeview.configure(yscroll=ysb.set)

        # Обновление данных когда фрейм видимый
        self.bind("<Visibility>", self.update_treeview_data)

        self.control.pack()
        self.treeview.pack()

    # Обновление данных
    def update_treeview_data(self, event=None):
        query = select(Member)
        result = self.session.execute(query).all()
        self.treeview.set_data(result)

    # Вызов окна добавления
    def add_data_command(self):
        MemberInputFrame(tk.Toplevel(),
                         self.session, self.add_data_handler).pack()

    # Вызов окна поиска
    def search_data_command(self):
        MemberInputFrame(tk.Toplevel(),
                         self.session, self.search_data_handler).pack()

    # Вызов окна редактирования
    def edit_data_command(self):
        iid, values = self.selected()
        frame = MemberInputFrame(tk.Toplevel(),
                                 self.session,
                                 self.edit_data_handler, iid)

        frame.name_entry.insert(0, values[0])
        frame.phone_entry.insert(0, str(values[1])[1:])
        frame.brith_entry.insert(0, values[2])
        frame.pack()

    # Команда на удаление
    @error_catcher
    def remove_data_command(self):
        query = delete(Member).where(Member.id == self.treeview.focus())
        self.session.execute(query)

    # Обработка добавления
    @error_catcher
    def add_data_handler(self, frame, *args, **kwargs):
        self.session.execute(insert(Member), [frame.get_data()])

    # Обработка поиска
    @error_catcher
    def search_data_handler(self, frame, *args, **kwargs):
        query = select(Member)

        name = frame.name()
        phone = frame.phone()
        brith = frame.brith()

        conditions = [
            (name, Member.name == name),
            (phone, Member.phone == phone),
            (brith, Member.brith == brith),
        ]

        for c in conditions:
            if c[0]:
                query.where(c[1])

        result = self.session.execute(query).all()
        self.treeview.set_data(result)

    # Обработка редактирования
    @error_catcher
    def edit_data_handler(self, frame, selected_id, *args, **kwargs):
        query = update(Member).where(Member.id == selected_id)
        query = query.values({
            **frame.get_data(),
            "updated_at": datetime.now()
        })
        self.session.execute(query)
