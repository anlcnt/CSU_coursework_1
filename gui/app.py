import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from gui.frames.members import MembersView
from gui.frames.books import BooksView
from gui.frames.lending import LendingView
from gui.frames.halls import HallsView
from gui.frames.report import ReportView


class App(tk.Frame):
    """GUI приложения"""

    def __init__(self, master, db_url="sqlite://"):
        super().__init__(master)
        # TODO: Конфигурация подключения
        engine = create_engine(db_url, echo=True)
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=engine))
        self.pack()

        self.tabControl = ttk.Notebook(self)
        membersTab = MembersView(self.tabControl, self.session)
        booksTab = BooksView(self.tabControl, self.session)
        lendingTab = LendingView(self.tabControl, self.session)
        hallTab = HallsView(self.tabControl, self.session)
        reportTab = ReportView(self.tabControl, self.session)

        self.tabControl.add(lendingTab, text="Выдача книг")
        self.tabControl.add(membersTab, text="Читательские билеты")
        self.tabControl.add(booksTab, text="Книги")
        self.tabControl.add(hallTab, text="Залы")
        self.tabControl.add(reportTab, text="Отчёт")
        self.tabControl.pack(expand=1, fill="both")

    
    def _create_session(self, url):
        pass
