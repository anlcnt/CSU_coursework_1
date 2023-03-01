import tkinter as tk
from tkinter import ttk
from sqlalchemy import select, update, insert, delete
from db.models.book import Book
from gui.treeviews.books import BooksTree


class BooksInputFrame(tk.Frame):
    ''' Фрейм ввода данных книги '''

    def __init__(self, master, handler=None, selected_id=None):
        super().__init__(master)

        ttk.Label(self, text="Название").grid(row=0, column=0)
        ttk.Label(self, text="Год издания").grid(row=1, column=0)
        ttk.Label(self, text="Автор").grid(row=2, column=0)
        ttk.Label(self, text="Издатель").grid(row=3, column=0)
        ttk.Label(self, text="Кол-во страниц").grid(row=4, column=0)
        ttk.Label(self, text="Полка").grid(row=5, column=0)

        self.name_entry = ttk.Entry(self)
        self.year_entry = ttk.Entry(self)
        self.pages_entry = ttk.Entry(self)
        self.author_combobox = ttk.Combobox(self)
        self.publisher_combobox = ttk.Combobox(self)
        self.field_combobox = ttk.Combobox(self)

        self.accept_button = ttk.Button(self, text="Выполнить")

        if handler is not None:
            self.accept_button.config(
                command=lambda: handler(self, selected_id))

        self.name_entry.grid(row=0, column=1)
        self.year_entry.grid(row=1, column=1)
        self.author_combobox.grid(row=2, column=1)
        self.publisher_combobox.grid(row=3, column=1)
        self.pages_entry.grid(row=4, column=1)
        self.field_combobox.grid(row=5, column=1)
        self.accept_button.grid(row=6, column=0)


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

    def update_treeview_data(self, event=None):
        query = select(Book)
        result = self.session.execute(query).all()
        self.treeview.set_data(result)

    def add_data_command(self):
        BooksInputFrame(tk.Toplevel(), self.add_data_handler).pack()

    def search_data_command(self):
        BooksInputFrame(tk.Toplevel(), self.search_data_handler).pack()

    def edit_data_command(self):
        selected_id = self.treeview.focus()
        values = self.treeview.item(selected_id)['values']

        frame = BooksInputFrame(
            tk.Toplevel(), self.add_data_handler, selected_id)

        frame.name_entry.insert(0, values[0])
        frame.author_combobox.insert(0, values[1])
        frame.publisher_combobox.insert(0, values[2])
        frame.year_entry.insert(0, str(values[3]))
        frame.pages_entry.insert(0, str(values[4]))
        frame.field_combobox.insert(0, values[5])

        frame.pack()

    def remove_data_command(self):
        query = delete(Book).where(Book.id == self.treeview.focus())
        self.session.execute(query)
        self.update_treeview_data()

    def add_data_handler(self, input_frame, *args, **kwargs):
        self.session.execute(insert(Book), [{
            "year": int(input_frame.year_entry.get()),
            "pages": int(input_frame.pages_entry.get()),
            "name": input_frame.name_entry.get()
        }])
        self.update_treeview_data()

    def search_data_handler(self, input_frame, *args, **kwargs):
        query = select(Book)

        name = input_frame.name_entry.get()
        year = input_frame.year_entry.get()
        pages = input_frame.pages_entry.get()

        if len(name):
            query = query.where(Book.name == name)
        if len(year):
            query = query.where(Book.year == year)
        if len(pages):
            query = query.where(Book.pages == pages)

        result = self.session.execute(query).all()
        self.treeview.set_data(result)

    def edit_data_handler(self, input_frame, selected_id, *args, **kwargs):
        pass
