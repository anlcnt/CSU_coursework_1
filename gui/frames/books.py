import tkinter as tk
from tkinter import ttk
from sqlalchemy import select, update, insert, delete
from db.models.book import Book
from db.models.author import Author
from db.models.publisher import Publisher
from db.models.field import Field
from gui.treeviews.books import BooksTree


class BooksInputFrame(tk.Frame):
    ''' Фрейм ввода данных книги '''

    def __init__(self, master, session, handler=None, selected_id=None):
        super().__init__(master)

        self.session = session

        labels = ["Название", "Год издания", "Автор",
                  "Издатель", "Кол-во страниц", "Полка"]

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
        self.accept_button = ttk.Button(self, text="Выполнить")

        if handler is not None:
            self.accept_button.config(
                command=lambda: handler(self, selected_id))

        def set_grid(e, i):
            return e.grid(row=i,
                          column=1,
                          sticky="e",
                          padx=(5, 5),
                          pady=(5, 5))

        set_grid(self.name_entry, 0)
        set_grid(self.year_entry, 1)
        set_grid(self.author_combobox, 2)
        set_grid(self.publisher_combobox, 3)
        set_grid(self.pages_entry, 4)
        set_grid(self.field_combobox, 5)
        set_grid(self.accept_button, 6)

        for i, label in enumerate(labels):
            ttk.Label(self, text=label).grid(row=i, column=0, sticky="e")

    def get_rows(self, model):
        query = select(model.name, model.id)
        result = self.session.execute(query).all()
        return dict(result)

    def author_id(self):
        return self.authors[self.author_combobox.get()]

    def field_id(self):
        return self.fields[self.field_combobox.get()]

    def publisher_id(self):
        return self.publishers[self.publisher_combobox.get()]

    def get_data(self):
        return {
            "year": int(self.year_entry.get()),
            "pages": int(self.pages_entry.get()),
            "author_id": self.author_id(),
            "publisher_id": self.publisher_id(),
            "fields_id": self.field_id(),
            "name": self.name_entry.get()
        }


class BooksView(tk.Frame):
    ''' Общий фрейм книг '''

    def __init__(self, master, session):
        super().__init__(master)
        self.session = session

        # Таблица
        self.treeview = BooksTree(self)
        y_scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.treeview.yview)
        self.treeview.configure(yscroll=y_scrollbar.set)

        # Обновление данных когда фрейм видимый
        # self.bind("<Visibility>", self.update_treeview_data)
        self.update_treeview_data()

        # Кнопки
        self.add_button = ttk.Button(self, text="Добавить")
        self.edit_button = ttk.Button(self, text="Изменить")
        self.remove_button = ttk.Button(self, text="Удалить")
        self.search_button = ttk.Button(self, text="Поиск")
        self.update_button = ttk.Button(self, text="Обновить")

        self.add_button.config(command=self.add_data_command)
        self.edit_button.config(command=self.edit_data_command)
        self.remove_button.config(command=self.remove_data_command)
        self.search_button.config(command=self.search_data_command)
        self.update_button.config(command=self.update_treeview_data)

        self.add_button.grid(row=0, column=0)
        self.edit_button.grid(row=0, column=1)
        self.search_button.grid(row=0, column=2)
        self.remove_button.grid(row=0, column=3)
        self.update_button.grid(row=0, column=4)
        self.treeview.grid(row=1, column=0, columnspan=5)

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
        selected_id = self.treeview.focus()
        values = self.treeview.item(selected_id)['values']

        frame = BooksInputFrame(
            tk.Toplevel(), self.session, self.edit_data_handler, selected_id)

        frame.name_entry.insert(0, values[0])
        frame.author_combobox.insert(0, values[1])
        frame.publisher_combobox.insert(0, values[2])
        frame.year_entry.insert(0, str(values[3]))
        frame.pages_entry.insert(0, str(values[4]))
        frame.field_combobox.insert(0, values[5])

        frame.pack()

    # Команда на удаление
    def remove_data_command(self):
        query = delete(Book).where(Book.id == self.treeview.focus())
        self.session.execute(query)
        self.update_treeview_data()

    # Обработка добавления
    def add_data_handler(self, frame, *args, **kwargs):
        self.session.execute(insert(Book), [frame.get_data()])
        self.update_treeview_data()

    # Обработка поиска
    def search_data_handler(self, frame, *args, **kwargs):
        query = select(Book)

        name = frame.name_entry.get()
        year = frame.year_entry.get()
        pages = frame.pages_entry.get()

        if len(name):
            query = query.where(Book.name == name)
        if len(year):
            query = query.where(Book.year == year)
        if len(pages):
            query = query.where(Book.pages == pages)
        if len(frame.author_combobox.get()):
            query = query.where(Book.author_id == frame.author_id())
        if len(frame.publisher_combobox.get()):
            query = query.where(Book.publisher_id == frame.publisher_id())
        if len(frame.field_combobox.get()):
            query = query.where(Book.field_id == frame.field_id())

        result = self.session.execute(query).all()
        self.treeview.set_data(result)

    # Обработка редактирования
    def edit_data_handler(self, frame, selected_id, *args, **kwargs):
        query = update(Book).where(Book.id == selected_id)
        query = query.values(**frame.get_data())
        self.session.execute(query)
        self.update_treeview_data()
