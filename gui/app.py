import tkinter as tk

from tkinter import ttk
from gui.treeviews.lending import LendingView
from gui.treeviews.member import MembersView


class App(tk.Frame):
    """GUI приложения"""

    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.tabControl = ttk.Notebook(self)

        tab1 = ttk.Frame(self.tabControl)
        tab2 = ttk.Frame(self.tabControl)

        self.tabControl.add(tab1, text="Выдача книг")
        self.tabControl.add(tab2, text="Читательские билеты")
        self.tabControl.pack(expand=1, fill="both")

        lending = LendingView(tab1)
        member = MembersView(tab2)

        lending.pack()
        member.pack()
