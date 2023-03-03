from gui.treeviews.base import BaseTree


months = ["Январь",
          "Февраль",
          "Март",
          "Апрель",
          "Май",
          "Июнь",
          "Июль",
          "Август",
          "Сентябрь",
          "Октябрь",
          "Ноябрь",
          "Декабрь"]


class ReportTree(BaseTree):
    ''' Таблица для отчётов '''

    def __init__(self, headers: dict, parent):
        super().__init__(headers, parent)

    def set_data(self, data):
        self.clear()

        for record in data:
            self.push(record)


class BookByYearTreeview(ReportTree):
    '''
        Выводит за каждый месяц года,
        определенного пользователем, количество выдач книг
    '''

    def __init__(self, parent):
        headers = {
            "month": "Месяц",
            "count": "Кол-во книг",
        }
        super().__init__(headers=headers, parent=parent)

    def push(self, record):
        self.insert(parent="", index="end", values=[
            months[record[0] - 1],
            record[1]
        ])


class OldestBooksTreeview(ReportTree):
    '''
        Выводит название и возраст книги самой старой книги в каждом из залов.
    '''

    def __init__(self, parent):
        headers = {
            "hall": "Зал",
            "book": "Книга",
            "field": "Область знаний",
            "year": "Год издания",
        }
        super().__init__(headers=headers, parent=parent)

    def push(self, record):
        print(record)
        self.insert(parent="", index="end", values=[
            record[2].hall.name,
            record[0].name,
            record[2].name,
            record[1],
        ])


class BestBooksTreeview(ReportTree):
    '''
        Выводит 5 лучших книг, которые за прошедший месяц
        пользовались наибольшим спросом.
    '''

    def __init__(self, parent):
        headers = {
            "book": "Книга",
            "count": "Кол-во",
        }
        super().__init__(headers=headers, parent=parent)

    def push(self, record):
        self.insert(parent="", index="end", values=[
            record[0].name,
            record[1]
        ])
