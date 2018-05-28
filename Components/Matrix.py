# -*- coding: utf-8 -*-
from tkinter import *
import numpy as np
import math


class Matrix(Frame):
    def __init__(self, *args, **kargs):
        Frame.__init__(self, *args, **kargs)
        self.current_item = (1, 1)
        self.size_width = IntVar()
        self.size_height = IntVar()
        self.size_width.set(3)
        self.size_height.set(3)
        self.make_widgets()
        self.matrix_model = np.zeros((self.size_width.get(), self.size_height.get()))
        self.update()

    "Создаем виджеты"

    def make_widgets(self):
        self.main_frame = Frame(self)
        self.canvas_frame = Frame(self.main_frame)
        self.canvas_frame.pack(fill=BOTH, expand=True, anchor="nw")
        self.canvas = Canvas(self.canvas_frame, width=200, height=200, bg="#ffffff", relief=GROOVE, bd=3, )

        self.canvas_scrolly = Scrollbar(self.canvas_frame, orient='vertical', command=self.canvas.yview)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas_scrolly.pack(side=RIGHT, fill=Y)
        self.canvas.configure(yscrollcommand=self.canvas_scrolly.set)

        self.canvas_scrollx = Scrollbar(self.main_frame, orient='horizontal', command=self.canvas.xview)
        self.canvas_scrollx.pack(fill=X)
        self.canvas.configure(xscrollcommand=self.canvas_scrollx.set)
        self.settings_field = Frame(self.main_frame)
        Label(self.settings_field, text="Размер матрицы ").pack(side=LEFT)
        self.size_box_width = Spinbox(self.settings_field, from_=0, to=100, width=5, textvariable=self.size_width,
                                      command=lambda: self.update_model(1))
        self.size_box_width.pack(side=LEFT)
        Label(self.settings_field, text=" на ").pack(side=LEFT)
        self.size_box_height = Spinbox(self.settings_field, from_=0, to=100, width=5, textvariable=self.size_height,
                                       command=lambda: self.update_model(0))
        self.size_box_height.pack(side=LEFT)
        Button(self.settings_field, text="Очистить").pack(side=BOTTOM)
        self.settings_field.pack()
        self.canvas.bind('<Button-1>', lambda x: self.chose_figure(x))
        self.canvas.bind('<KeyPress>', self.keydown)
        self.canvas.bind('<space>', lambda x: self.move())
        self.last_width_box = int(self.size_box_width.get())
        self.last_heigth_box = int(self.size_box_height.get())
        self.main_frame.pack(fill=BOTH, expand=True)
        self.canvas.focus_set()

    """Переход на следующую ячейку"""

    def move(self):
        # Передвижение фокуса ввода
        if (self.matrix_model.shape[0] != self.current_item[0] and self.matrix_model.shape[1] >= self.current_item[1]):
            self.current_item = (self.current_item[0] + 1, self.current_item[1])
        else:
            self.current_item = (1, self.current_item[1] + 1)
        if self.current_item[0] > self.matrix_model.shape[0] or self.current_item[1] > self.matrix_model.shape[1]:
            self.current_item = self.matrix_model.shape
        self.update()

    """Событие ввода цифр в матрицу"""

    def keydown(self, event):
        if event.char.isdecimal():
            key = int(event.char)
            self.matrix_model[self.current_item[1] - 1, self.current_item[0] - 1] = self.matrix_model[
                                                                                        self.current_item[1] - 1,
                                                                                        self.current_item[
                                                                                            0] - 1] * 10 + key
            self.update()
            # self.move()

    """Выбор чисел"""

    def chose_figure(self, event):
        x_cord = math.ceil((event.x) / 30)
        y_cord = math.ceil((event.y) / 30)
        if x_cord <= self.matrix_model.shape[1] and y_cord <= self.matrix_model.shape[
            0]:  # Если мы попадаем в размер, то все хорошо, если нет то и не надо
            # Рисуем квадратик
            self.canvas.delete(ALL)
            self.draw_matrix()
            self.set_focus(x_cord, y_cord)

    """Обновляем все поле"""

    def update(self):
        self.canvas.delete(ALL)
        self.draw_matrix()
        self.set_focus(self.current_item[0], self.current_item[1])
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

    """Возврашаем модель матрицы"""

    def get_model(self):
        return self.matrix_model

    "Перемещаем красный квадратик на соседнюю пустую ячейку"

    def set_focus(self, x_cord, y_cord):
        self.canvas.create_rectangle((x_cord-1) * 30 - 10, (y_cord-1) * 30 - 10, (x_cord-1) * 30 + 10, (y_cord-1) * 30 + 10,
                                     outline="red")
        self.current_item = (x_cord, y_cord)

    """Обновление модели"""

    def update_model(self, axis):
        if axis:
            if self.matrix_model.shape[1] > int(self.size_box_width.get()):
                self.matrix_model = self.matrix_model[:, 1:]
            elif self.matrix_model.shape[1] == int(self.size_box_width.get()):
                if self.last_width_box > int(self.size_box_width.get()):
                    self.matrix_model = self.matrix_model[:, 1:]
                else:
                    extended_array = np.zeros((int(self.size_box_height.get()), 1))
                    self.matrix_model = np.concatenate((self.matrix_model, extended_array), axis=1)
            else:
                extended_array = np.zeros((int(self.size_box_height.get()), 1))
                self.matrix_model = np.concatenate((self.matrix_model, extended_array), axis=1)
            self.last_width_box = int(self.size_box_width.get())
        else:
            if self.matrix_model.shape[0] >= int(self.size_box_height.get()):
                self.matrix_model = self.matrix_model[1:, :]
            else:
                super_extended_array = np.zeros((1, int(self.size_box_width.get())))
                self.matrix_model = np.concatenate((self.matrix_model, super_extended_array), axis=0)
            self.last_heigth_box = (self.size_box_height.get())
        self.update()

    """Рисуем матрицу на канве"""

    def draw_matrix(self):
        for i in range(self.matrix_model.shape[0]):
            for j in range(self.matrix_model.shape[1]):
                self.canvas.create_text(30 * j, 30 * i, text=str(self.matrix_model[i, j])[:-2])
