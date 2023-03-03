import tkinter as tk
from tkinter import ttk

from db.models.member import Member
from db.queries import reports as queries
from gui.treeviews import reports as treeviews
from sqlalchemy import select
from datetime import date


class ReportFrame(tk.Frame):
    ''' Базовый фрейм отчёта '''

    def __init__(self, master, treeview, session, description=None):
        super().__init__(master)
        self.session = session
        self.treeview = treeview(self)

        if description:
            ttk.Label(self, text=description, anchor="e").pack()

        self.treeview.pack(side=tk.BOTTOM)
        self.bind("<Visibility>", self.update_treeview_data)

    def update_treeview_data(self):
        pass

    def get_rows(self, model):
        query = select(model.name, model)
        result = self.session.execute(query).all()
        return dict(result)


class BookByYearView(ReportFrame):
    '''
        Выводит за каждый месяц года,
        определенного пользователем, количество выдач книг
    '''

    def __init__(self, master, session):
        super().__init__(master,
                         treeviews.BookByYearTreeview,
                         session,
                         'Посчитать за каждый месяц года, '
                         'определенного пользователем, количество выдач книг')

        self.members = self.get_rows(Member)
        self.year_var = tk.IntVar(value=2015)

        control = tk.Frame(self)
        self.accept_button = ttk.Button(control, text="Выполнить")
        self.members_combobox = ttk.Combobox(
            control, values=tuple(self.members.keys()))
        self.year_spinbox = ttk.Spinbox(control,
                                        from_=0,
                                        to=date.today().year,
                                        textvariable=self.year_var)

        self.accept_button.config(command=self.update_treeview_data)

        self.accept_button.pack(side=tk.RIGHT)
        self.members_combobox.pack(side=tk.LEFT)
        self.year_spinbox.pack(side=tk.RIGHT)
        control.pack()

    def update_treeview_data(self, event=None):
        member = self.members[self.members_combobox.get()]
        query = queries.books_by_year(member, self.year_var.get())
        result = self.session.execute(query)
        self.treeview.set_data(result)


class OldestBooksView(ReportFrame):
    '''
        Выводит название и возраст книги самой старой книги в каждом из залов.
    '''

    def __init__(self, master, session):
        super().__init__(master,
                         treeviews.OldestBooksTreeview,
                         session,
                         'Вывести название и возраст книги '
                         'самой старой книги в каждом из залов.')

    def update_treeview_data(self, event=None):
        query = queries.oldest_books()
        result = self.session.execute(query).all()
        self.treeview.set_data(result)


class BestBooksView(ReportFrame):
    '''
        Выводит 5 лучших книг, которые за прошедший месяц
        пользовались наибольшим спросом.
    '''

    def __init__(self, master, session):
        super().__init__(master,
                         treeviews.BestBooksTreeview,
                         session,
                         'Вывести 5 лучших книг, которые за прошедший месяц '
                         'пользовались наибольшим спросом.')

    def update_treeview_data(self, event=None):
        query = queries.best_books_by_current_month()
        result = self.session.execute(query).all()
        self.treeview.set_data(result)


class ReportView(tk.Frame):
    '''Фрейм отчётов'''

    def __init__(self, master, session):
        super().__init__(master)

        self.tabControl = ttk.Notebook(self)
        booksByYear = BookByYearView(self.tabControl, session)
        oldestBooks = OldestBooksView(self.tabControl, session)
        bestBooks = BestBooksView(self.tabControl, session)

        self.tabControl.add(booksByYear, text="Книги за год")
        self.tabControl.add(oldestBooks, text="Старейшие книги")
        self.tabControl.add(bestBooks, text="Лучшие книги месяца")
        self.tabControl.pack(expand=1, fill="both")
