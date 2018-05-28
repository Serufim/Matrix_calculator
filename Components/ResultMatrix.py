# -*- coding: utf-8 -*-
from tkinter import *
import numpy as np
import math


class ResultMatrix(Frame):
    def __init__(self, *args, **kargs):
        Frame.__init__(self, *args, **kargs)
        self.current_item = (1, 1)
        self.size_width = IntVar()
        self.size_height = IntVar()
        self.size_width.set(3)
        self.size_height.set(3)
        self.make_widgets()
        self.matrix_model = np.zeros((self.size_width.get(), self.size_height.get()))

    "Создаем виджеты"

    def make_widgets(self):
        self.main_frame = Frame(self)
        self.canvas = Canvas(self.main_frame, width=200, height=200, bg="#ffffff", relief=GROOVE, bd=3, )
        self.canvas.pack(fill=BOTH, expand=True)
        self.main_frame.pack(fill=BOTH, expand=True)
        self.canvas.focus_set()

    """Задает матрицу из вне"""

    def set_model(self, model):
        self.matrix_model = model
        self.draw_matrix()

    """Рисуем матрицу на канве"""

    def draw_matrix(self):
        self.canvas.delete(ALL)
        for i in range(self.matrix_model.shape[0]):
            for j in range(self.matrix_model.shape[1]):
                self.canvas.create_text(30 + 40 * j, 30 + 40 * i, text=str(self.matrix_model[i, j])[:-2])
