import tkinter as tk
from tkinter import ttk
from sqlalchemy import select
from db.models.book import Book
from gui.treeviews.books import BooksTree


class BooksView(tk.Frame):
    '''Фрейм книг'''

    def __init__(self, master, session):
        super().__init__(master)
        self.session = session

        add_button = tk.Button(self, text="Добавить")
        add_button.pack()


        # Таблица
        self.treeview = BooksTree(self)
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscroll=ysb.set)
        self.treeview.pack()

        # Обновление данных когда фрейм видимый
        self.bind("<Visibility>", self.update_treeview_data)

    def update_treeview_data(self, event):
        query = select(Book)
        result = self.session.execute(query).all()
        self.treeview.set_data(result)