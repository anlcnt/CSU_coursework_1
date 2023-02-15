import tkinter as tk
from tkinter import ttk
from sqlalchemy import select
from db.models.hall import Hall
from gui.treeviews.halls import HallsTree


class HallsView(tk.Frame):
    '''Фрейм книг'''

    def __init__(self, master, session):
        super().__init__(master)
        self.session = session

        self.treeview = HallsTree(self)
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscroll=ysb.set)
        self.treeview.pack()

        # Обновление данных когда фрейм видимый
        self.bind("<Visibility>", self.update_treeview_data)

    def update_treeview_data(self, event):
        query = select(Hall)
        result = self.session.execute(query).all()
        self.treeview.set_data(result)