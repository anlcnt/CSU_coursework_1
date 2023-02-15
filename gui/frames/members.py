import tkinter as tk
from tkinter import ttk
from sqlalchemy import select
from db.models.member import Member
from gui.treeviews.members import MembersTree


class MembersView(tk.Frame):
    '''Фрейм читателей'''

    def __init__(self, master, session):
        super().__init__(master)
        self.session = session

        self.treeview = MembersTree(self)
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscroll=ysb.set)
        self.treeview.pack()

        # Обновление данных когда фрейм видимый
        self.bind("<Visibility>", self.update_treeview_data)

    def update_treeview_data(self, event):
        query = select(Member)
        result = self.session.execute(query).all()
        self.treeview.set_data(result)