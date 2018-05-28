# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import Components.ResultMatrix as ResultMatrix
import Components.Matrix as Matrix


def plus_this():
    try:
        result = f1.get_model() + f2.get_model()
        f3.set_model(result)
        nb.select(2)
    except:
        messagebox.showerror("Ошибка!!!", "Невозможно провести операцию, внимательно проверьте входные условия")


def minus_this():
    try:
        result = f1.get_model() - f2.get_model()
        f3.set_model(result)
        nb.select(2)
    except:
        messagebox.showerror("Ошибка!!!", "Невозможно провести операцию, внимательно проверьте входные условия")


def multiple_this():
    try:
        result = f1.get_model().dot(f2.get_model())
        f3.set_model(result)
        nb.select(2)
    except:
        messagebox.showerror("Ошибка!!!", "Невозможно провести операцию, внимательно проверьте входные условия")


if __name__ == '__main__':
    root = Tk()
    root.title('test')

    nb = ttk.Notebook(root)
    nb.pack(fill='both', expand='yes', side=LEFT)

    f3 = ResultMatrix.ResultMatrix(root)
    f2 = Matrix.Matrix(root)
    f1 = Matrix.Matrix(root)

    nb.add(f1, text='Матрица A')
    nb.add(f2, text='Матрица B')
    nb.add(f3, text='Матрица C')
    control_panel = Frame(root)
    Label(control_panel, text="Действия").pack(fill=X, side=TOP)
    Button(control_panel, text="Сложение", command=lambda: plus_this()).pack()
    Button(control_panel, text="Вычитание", command=lambda: minus_this()).pack()
    Button(control_panel, text="Умножение", command=lambda: multiple_this()).pack()
    control_panel.pack(side=RIGHT, anchor='nw', padx=10)

    root.mainloop()
