import tkinter as tk
from tkinter import ttk


class ReportView(tk.Frame):
    '''Фрейм отчёта'''

    def __init__(self, master, session):
        super().__init__(master)
        self.session = session
