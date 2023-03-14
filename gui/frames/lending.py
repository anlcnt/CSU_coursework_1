import tkinter as tk
from tkinter import ttk
from datetime import datetime
from sqlalchemy import select, insert, update
from gui.treeviews.lending import LendingTree
from db.models.lending import Lending
from db.models.member import Member
from db.models.book import Book
from gui.frames.base import BaseView, BaseInputFrame as BIF, error_catcher


class LendingInputFrame(BIF):
    ''' Фрейм ввода данных выдачи книг '''

    def __init__(self, master, session, handler):
        labels = ["Читатель", "Книга", "Дата выдачи"]

        super().__init__(master, session, labels, handler)

        self.members = self.get_rows(Member)
        self.books = self.get_rows(Book)

        self.member_combobox = ttk.Combobox(self,
                                            values=list(self.members.keys()))
        self.book_combobox = ttk.Combobox(self,
                                          values=list(self.books.keys()))
        self.lended_at_entry = ttk.Entry(self)
        self.accept_button = ttk.Button(self, text="Выполнить")

        now = datetime.now().strftime("%d.%m.%Y")
        self.lended_at_entry.insert(0, now)
        self.accept_button.config(command=lambda: handler(self))

        BIF.set_grid(self.member_combobox, 0)
        BIF.set_grid(self.book_combobox, 1)
        BIF.set_grid(self.lended_at_entry, 2)
        BIF.set_grid(self.accept_button, 3)

    def book_id(self):
        book = self.book_combobox.get()
        if book in self.books.keys():
            return self.books[book]
        raise ValueError("Такая книга отсутствует в базе")

    def member_id(self):
        member = self.member_combobox.get()
        if member in self.members.keys():
            return self.members[member]
        raise ValueError("Такой читатель отсутствует в базе")

    def lending_date(self):
        value = self.lended_at_entry.get()
        if value:
            try:
                return datetime.strptime(value, "%d.%m.%Y")
            except ValueError:
                raise("Неверный формат даты")
        return None

    def get_data(self):
        return {
            "member_id": self.member_id(),
            "book_id": self.book_id(),
            "lended_at": self.lending_date()
        }


class LendingControl(tk.Frame):
    ''' Фрейм управления выдачей книг '''

    def __init__(self, master):
        super().__init__(master)

        self.rent_button = ttk.Button(self, text="Выдать книгу")
        self.close_lending_button = ttk.Button(self, text="Закрыть выдачу")
        self.update_button = ttk.Button(self, text="Обновить")
        self.open_check = ttk.Checkbutton(self,
                                          text="Только не закрытые выдачи",
                                          variable=master.only_open)

        self.rent_button.config(command=master.rent_book_command)
        self.close_lending_button.config(command=master.close_rent_command)
        self.update_button.config(command=master.update_treeview_data)
        self.open_check.config(command=master.update_treeview_data)

        self.rent_button.pack(side=tk.LEFT)
        self.close_lending_button.pack(side=tk.LEFT)
        self.update_button.pack(side=tk.LEFT)
        self.open_check.pack(side=tk.LEFT)


class LendingView(BaseView):
    '''Фрейм выдачи книг'''

    def __init__(self, master, session):
        super().__init__(master, session)

        # Управление
        self.only_open = tk.IntVar()
        self.control = LendingControl(self)

        # Таблица
        self.treeview = LendingTree(self)
        ysb = ttk.Scrollbar(self,
                            orient=tk.VERTICAL,
                            command=self.treeview.yview)
        self.treeview.configure(yscroll=ysb.set)

        # Обновление данных когда фрейм видимый
        self.bind("<Visibility>", self.update_treeview_data)

        self.control.pack()
        self.treeview.pack(expand=True)

    def update_treeview_data(self, event=None):
        query = select(Lending)

        if self.only_open.get():
            query = query.where(Lending.returned_at == None)

        result = self.session.execute(query).all()
        self.treeview.set_data(result)

    def rent_book_command(self):
        LendingInputFrame(tk.Toplevel(),
                          self.session, self.rent_book_handler).pack()

    @error_catcher
    def close_rent_command(self):
        query = update(Lending).where(Lending.id == self.treeview.focus())
        query = query.values({"returned_at": datetime.now()})
        self.session.execute(query)

    @error_catcher
    def rent_book_handler(self, frame, *args, **kwargs):
        self.session.execute(insert(Lending), [{
            **frame.get_data(),
            "returned_at": None
        }])
