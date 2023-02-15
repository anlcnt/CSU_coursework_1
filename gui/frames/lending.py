import tkinter as tk
from tkinter import ttk
from sqlalchemy import select
from gui.treeviews.lending import LendingTree
from db.models.lending import Lending


class LendingView(tk.Frame):
    '''Фрейм выдачи книг'''

    def __init__(self, master, session):
        super().__init__(master)
        self.session = session

        self.treeview = LendingTree(self)
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscroll=ysb.set)
        self.treeview.pack()

        # Обновление данных когда фрейм видимый
        self.bind("<Visibility>", self.update_treeview_data)

    def update_treeview_data(self, event):
        query = select(Lending)
        result = self.session.execute(query).all()
        self.treeview.set_data(result)
