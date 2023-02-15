import configparser

from tkinter import Tk
from gui.app import App


def run_app():
    root = Tk()
    app = App(root, 'sqlite:///base.db')
    app.mainloop()


if __name__ == '__main__':
    run_app()
