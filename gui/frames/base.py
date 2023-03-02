import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from sqlalchemy import select, insert


# Отлов ошибок
def error_catcher(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            func(*args, **kwargs)
        except ValueError as e:
            showerror(message="Не удалось создать запись." + str(e))
            self.session.rollback()
        else:
            self.session.commit()
            self.update_treeview_data()
    return wrapper


class BaseInputFrame(tk.Frame):
    ''' Базовый фрейм ввода данных '''

    def __init__(self, master, session, labels,
                 handler=None, selected_id=None):
        super().__init__(master)
        self.session = session

        self.accept_button = ttk.Button(self, text="Выполнить")

        if handler is not None:
            self.accept_button.config(
                command=lambda: handler(self, selected_id))

        for i, label in enumerate(labels):
            ttk.Label(self, text=label).grid(row=i, column=0, sticky="e")

    # Возвращает данные для combobox
    def get_rows(self, model):
        query = select(model.name, model.id)
        result = self.session.execute(query).all()
        return dict(result)

    # Создаёт новую запись
    def create_new_record(self, model, **data):
        return self.session.execute(insert(model), [data])

    @staticmethod
    def set_grid(e, i):
        return e.grid(row=i,
                      column=1,
                      sticky="e",
                      padx=(5, 5),
                      pady=(5, 5))


class BaseView(tk.Frame):
    ''' Базовый фрейм представления '''

    def __init__(self, master, session):
        super().__init__(master)
        self.session = session

        self.control = ttk.Frame(self)

        # Кнопки
        self.add_button = ttk.Button(self.control, text="Добавить")
        self.edit_button = ttk.Button(self.control, text="Изменить")
        self.remove_button = ttk.Button(self.control, text="Удалить")
        self.search_button = ttk.Button(self.control, text="Поиск")
        self.update_button = ttk.Button(self.control, text="Обновить")

        self.add_button.config(command=self.add_data_command)
        self.edit_button.config(command=self.edit_data_command)
        self.remove_button.config(command=self.remove_data_command)
        self.search_button.config(command=self.search_data_command)
        self.update_button.config(command=self.update_treeview_data)

        self.add_button.pack(side=tk.LEFT)
        self.edit_button.pack(side=tk.LEFT)
        self.search_button.pack(side=tk.LEFT)
        self.remove_button.pack(side=tk.LEFT)
        self.update_button.pack(side=tk.LEFT)

        self.control.pack()

    # Вызов окна добавления
    def add_data_command(self):
        pass

    # Вызов окна поиска
    def search_data_command(self):
        pass

    # Вызов окна редактирования
    def edit_data_command(self):
        pass

    # Команда на удаление
    @error_catcher
    def remove_data_command(self):
        pass

    # Обработка добавления
    @error_catcher
    def add_data_handler(self, frame, *args, **kwargs):
        pass

    # Обработка поиска
    @error_catcher
    def search_data_handler(self, frame, *args, **kwargs):
        pass

    # Обработка редактирования
    @error_catcher
    def edit_data_handler(self, frame, selected_id, *args, **kwargs):
        pass
