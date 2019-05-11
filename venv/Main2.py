# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 00:53:21 2019

@author: dell
"""

from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from functools import partial
import parser
import random
import timeit
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from matplotlib.ticker import NullFormatter
import re


# TODO : adding trigonometry parsing
def evaluate_equation(formula, x):
    code = parser.expr(formula).compile()
    return eval(code)


class Main:
    # GUI init.
    def __init__(self, master):
        self.current_method = "Gaussian-elimination"
        width = 800
        height = 700
        x = (master.winfo_screenwidth() // 2) - (width // 2)
        y = (master.winfo_screenheight() // 2) - (height // 2)
        master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        master.title('Roots of Polynomials')
        frame = Frame(master)
        frame.configure(background='black')

        label_1 = Label(master, text="Equations: ", font="verdana 10 bold", bg="#212F3C", fg="#16A085")
        label_1.place(x=50, y=170)

        self.function_entry = Text(master, height=6, width=33)
        self.function_entry.place(x=150, y=170)

        label_1 = Label(master, text="Method: ", font="verdana 10 bold", bg="#212F3C", fg="#16A085")
        label_1.place(x=50, y=300)

        # Create a Tkinter variable
        tkvar = StringVar(master)

        # Dictionary with options
        choices = {'Gaussian-elimination', ' LU decomposition', 'Gaussian-Jordan', 'Gauss-Seidel'}
        tkvar.set('Gaussian-elimination')  # set the default option

        self.popupMenu = OptionMenu(master, tkvar, *choices, command=self.method_to_use)
        self.popupMenu.place(x=150, y=295)
        self.popupMenu["bg"] = "#16A085"

        label = Label(master, text="#.# Roots of Polynomials #.#", font="verdana 20 bold", bg="#212F3C", pady=20,
                      fg="#16A085")
        label.place(x=200, y=0)

        label = Label(master, text="Read from file (Insert file name) :", font="verdana 10 bold", bg="#212F3C", pady=20,
                      fg="#16A085")
        label.place(x=50, y=100)

        label = Label(master, text="(OR)", font="verdana 10 bold", bg="#212F3C", pady=20,
                      fg="#16A085")
        label.place(x=0, y=120)

        self.file_entry = Entry(master)
        self.file_entry.place(x=320, y=120, width=100)

        b = Button(master, text="Get Roots", command=self.solve, bg="#16A085", font="verdana 10 bold", fg="#212F3C")
        b.place(x=380, y=370)

        self.formula_as_str = ""

    def method_to_use(self, value):
        self.current_method = value

    def solve(self):
        s = self.function_entry.get('1.0', END)
        list = s.split("\n")
        print(list)
        m, b1 = self.parse_equations(list)
        print(m)
        print(b1)

    def parse_equations(self, list_of_strings):
        list_of_variables = []
        matrix = []
        b = []
        for j in range(len(list_of_strings)-1):
            list_of_coefficients = []
            result = 0
            txt = list_of_strings[j]
            x = re.findall("(([+-])?([\d]*)?([\w])+)|((=)(-)?([\d]+))", txt)
            for i in range(len(list_of_strings)+1):
                if x[i][5] == "=":
                    if x[i][6] == "-":
                        t = float(x[i][7]) * -1
                    else:
                        t = float(x[i][7])
                    result = t
                else:
                    if x[i][2] == '':
                        t = 1.0
                    else:
                        t = float(x[i][2])
                    if x[i][1] == "-":
                        list_of_coefficients.append(t * -1)
                    else:
                        list_of_coefficients.append(t)
                    list_of_variables.append(x[i][3])
                    print(list_of_coefficients)
            matrix.append(list_of_coefficients)
            b.append(result)
        return matrix, b


# tkinter main GUI window
root = Tk()
b = Main(root)
root["bg"] = "#212F3C"
root.mainloop()
