import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askstring
from datetime import datetime
from sqlalchemy import select, update, insert, delete
from db.models.book import Book
from db.models.author import Author
from db.models.publisher import Publisher
from db.models.field import Field
from gui.treeviews.books import BooksTree
from gui.frames.base import BaseView, BaseControl, BaseInputFrame as BIF, error_catcher


class BooksInputFrame(BIF):
    ''' Фрейм ввода данных книги '''

    def __init__(self, master, session, handler=None, selected_id=None):
        labels = ["Название", "Год издания", "Автор",
                  "Издатель", "Кол-во страниц", "Обл. знаний"]

        super().__init__(master, session, labels, handler, selected_id)

        self.authors = self.get_rows(Author)
        self.fields = self.get_rows(Field)
        self.publishers = self.get_rows(Publisher)

        self.name_entry = ttk.Entry(self, width=40)
        self.year_entry = ttk.Entry(self, width=40)
        self.pages_entry = ttk.Entry(self, width=40)
        self.author_combobox = ttk.Combobox(
            self, width=37, values=list(self.authors.keys()))
        self.publisher_combobox = ttk.Combobox(
            self, width=37, values=list(self.publishers.keys()))
        self.field_combobox = ttk.Combobox(
            self, width=37, values=list(self.fields.keys()))

        BIF.set_grid(self.name_entry, 0)
        BIF.set_grid(self.year_entry, 1)
        BIF.set_grid(self.author_combobox, 2)
        BIF.set_grid(self.publisher_combobox, 3)
        BIF.set_grid(self.pages_entry, 4)
        BIF.set_grid(self.field_combobox, 5)
        BIF.set_grid(self.accept_button, 6)

    def author_id(self):
        author = self.author_combobox.get()

        if author in self.authors.keys():
            return self.authors[self.author_combobox.get()]

        if askyesno(message="Указанный автор отсутствует. Создать?"):
            self.create_new_record(Author, name=author)
            return len(self.authors) + 1

        raise ValueError("Указанный автор отсутствует в базе")

    def field_id(self):
        field = self.field_combobox.get()

        if field in self.fields.keys():
            return self.fields[self.field_combobox.get()]

        raise ValueError("Указанная область знаний отсутствует в базе")

    def publisher_id(self):
        publisher = self.publisher_combobox.get()

        if publisher in self.publishers.keys():
            return self.publishers[self.publisher_combobox.get()]

        if askyesno(message="Указанный издатель отсутствует. Создать?"):
            place = askstring("Город",
                              "Укажите город издателя",
                              initialvalue="Москва")
            if not place:
                raise ValueError("Создание издателя отменено")
            self.create_new_record(Publisher, name=publisher, place=place)
            return len(self.publishers) + 1

        raise ValueError("Указанный издатель отсутствует в базе")

    def get_data(self):
        return {
            "year": int(self.year_entry.get()),
            "pages": int(self.pages_entry.get()),
            "author_id": self.author_id(),
            "publisher_id": self.publisher_id(),
            "fields_id": self.field_id(),
            "name": self.name_entry.get(),
            "updated_at": datetime.now()
        }


class BooksView(BaseView):
    ''' Общий фрейм книг '''

    def __init__(self, master, session):
        super().__init__(master, session)

        # Управление
        self.control = BaseControl(self)

        # Таблица
        self.treeview = BooksTree(self)
        y_scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.treeview.yview)
        self.treeview.configure(yscroll=y_scrollbar.set)

        # Обновление данных когда фрейм видимый
        self.bind("<Visibility>", self.update_treeview_data)

        self.control.pack()
        self.treeview.pack()

    # Обновление данных
    def update_treeview_data(self, event=None):
        query = select(Book)
        result = self.session.execute(query).all()
        self.treeview.set_data(result)

    # Вызов окна добавления
    def add_data_command(self):
        BooksInputFrame(tk.Toplevel(),
                        self.session, self.add_data_handler).pack()

    # Вызов окна поиска
    def search_data_command(self):
        BooksInputFrame(tk.Toplevel(),
                        self.session, self.search_data_handler).pack()

    # Вызов окна редактирования
    def edit_data_command(self):
        iid, values = self.selected()
        frame = BooksInputFrame(tk.Toplevel(),
                                self.session,
                                self.edit_data_handler, iid)

        frame.name_entry.insert(0, values[0])
        frame.author_combobox.insert(0, values[1])
        frame.publisher_combobox.insert(0, values[2])
        frame.year_entry.insert(0, str(values[3]))
        frame.pages_entry.insert(0, str(values[5]))
        frame.field_combobox.insert(0, values[6])
        frame.pack()

    # Команда на удаление
    @error_catcher
    def remove_data_command(self):
        query = delete(Book).where(Book.id == self.treeview.focus())
        self.session.execute(query)

    # Обработка добавления
    @error_catcher
    def add_data_handler(self, frame, *args, **kwargs):
        self.session.execute(insert(Book), [frame.get_data()])

    # Обработка поиска
    @error_catcher
    def search_data_handler(self, frame, *args, **kwargs):
        query = select(Book)

        name = frame.name_entry.get()
        year = frame.year_entry.get()
        pages = frame.pages_entry.get()
        author = frame.author_combobox.get()
        publisher = frame.publisher_combobox.get()
        field = frame.field_combobox.get()

        conditions = [
            (name, Book.name == name),
            (year, Book.year == year),
            (pages, Book.pages == pages),
            (author, Book.author_id == frame.author_id()),
            (publisher, Book.publisher_id == frame.publisher_id()),
            (field, Book.field_id == frame.field_id())
        ]

        for c in conditions:
            if c[0]:
                query.where(c[1])

        result = self.session.execute(query).all()
        self.treeview.set_data(result)

    # Обработка редактирования
    @error_catcher
    def edit_data_handler(self, frame, selected_id, *args, **kwargs):
        query = update(Book).where(Book.id == selected_id)
        query = query.values({
            **frame.get_data(),
            "updated_at": datetime.now()
        })
        self.session.execute(query)
