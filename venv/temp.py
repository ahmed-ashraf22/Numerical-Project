# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 00:53:21 2019

@author: dell
"""

import _ssl
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import time as tm
from functools import partial
import parser


# TODO : adding trigonometry parsing
def evaluate_equation(formula, x):
    code = parser.expr(formula).compile()
    return eval(code)


class Iterator(object):
    def __init__(self, limits=[]):
        self.limits = limits
        self.__i = -1

    def __next(self):
        self.__i = self.__i + 1
        if self.__i > self.limits.__len__():
            self.__i = self.limits.__len__()-1
        return self.limits[self.__i]

    def __prev(self):
        self.__i = self.__i - 1
        if self.__i < 0:
            self.__i = 0
        return self.limits[self.__i]


class Main:
    def __init__(self, master):
        self.current_method = "Bisection"
        width = 800
        height = 600
        x = (master.winfo_screenwidth() // 2) - (width // 2)
        y = (master.winfo_screenheight() // 2) - (height // 2)
        master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        master.title('Numerical Methods')
        frame = Frame(master)
        frame.configure(background='black')

        label_1 = Label(master, text="Function: ", font="verdana 10 bold", bg="#212F3C", fg="#16A085")
        label_1.place(x=50, y=120)

        self.function_entry = Entry(master)
        self.function_entry.place(x=150, y=120, width=200)

        label_1 = Label(master, text="Method: ", font="verdana 10 bold", bg="#212F3C", fg="#16A085")
        label_1.place(x=50, y=170)

        label_2 = Label(master, text="Max. NO. Iterations: ", font="verdana 10 bold", bg="#212F3C", fg="#16A085")
        label_2.place(x=50, y=220)

        label_3 = Label(master, text="Epsilon: ", font="verdana 10 bold", bg="#212F3C", fg="#16A085")
        label_3.place(x=380, y=220)

        self.epsilon_entry = Entry(master)
        self.epsilon_entry.place(x=460, y=220, width=50)

        self.max_entry = Entry(master)
        self.max_entry.place(x=220, y=220, width=50)

        x0 = Label(master, text="X0: ", font="verdana 10 bold", bg="#212F3C", fg="#16A085")
        x0.place(x=50, y=270)

        self.x0_entry = Entry(master)
        self.x0_entry.place(x=100, y=270, width=50)

        x1 = Label(master, text="X1: ", font="verdana 10 bold", bg="#212F3C", fg="#16A085")
        x1.place(x=172, y=270)

        self.x1_entry = Entry(master)
        self.x1_entry.place(x=220, y=270, width=50)

        b = Button(master, text="Solve", command=self.solve, bg="#16A085", font="verdana 10 bold", fg="#212F3C")
        b.place(x=380, y=320)



        # Create a Tkinter variable
        tkvar = StringVar(master)

        # Dictionary with options
        choices = {'Bisection', 'False-Position', 'Fixed Point', 'Newton-Raphson', 'Secant', 'Bierge-Vieta'}
        tkvar.set('Bisection')  # set the default option

        self.popupMenu = OptionMenu(master, tkvar, *choices, command=self.method_to_use)
        self.popupMenu.place(x=150, y=165)
        self.popupMenu["bg"] = "#16A085"

        label = Label(master, text="#.# Numerical Methods #.#", font="verdana 20 bold", bg="#212F3C", pady=20,
                      fg="#16A085")
        label.place(x=200, y=10)

    def method_to_use(self, value):
        self.current_method = value

    def solve(self):
        formula_as_str = self.function_entry.get()
        max_iter = self.max_entry.get()
        x1 = self.x0_entry.get()
        x2 = self.x1_entry.get()
        eps = self.epsilon_entry.get()
        if self.current_method == "Bisection":
            method = Bisection(formula_as_str, x1, x2, max_iter, eps)
        # elif self.current_method == "Newton-Raphson":
        #     method = NewtonRaphson(formula_as_str, x1, x2, max_iter, eps)
        # elif self.current_method == "False-Position":
        #     method = FalsePosition(formula_as_str, x1, x2, max_iter, eps)
        # elif self.current_method == "Fixed Point":
        #     method = FixedPoint(formula_as_str, x1, x2, max_iter, eps)
        # elif self.current_method == "Secant":
        #     method = Secant(formula_as_str, x1, x2, max_iter, eps)
        # else:
        #     method = BiergeVieta(formula_as_str, x1, x2, max_iter, eps)
        print(formula_as_str)
        result, number_of_iterations, errors, time, precision, values = method.solve()
        print(result)
        print(number_of_iterations)
        print(errors)
        print(time)
        print(precision)
        print(values)

        # Plotting
        plt.figure(1)
        plt.title("Bisection Method")
        plt.xlabel("X")
        plt.ylabel("F(X)")
        x1 = np.linspace(0, 0.12)
        y1 = self.function(x1)
        plt.ylim(-0.0003, 0.0003)
        plt.plot(x1, y1, "r-*")
        plt.show(block=False)

        iteration_label = Label(text="Iterations: ", font="verdana 10 bold", bg="#212F3C", pady=20,
                      fg="#16A085")
        iteration_label.place(x=50, y=360)
        n = Button(text="-->", command=right_arrow, bg="#16A085", font="verdana 10 bold", fg="#212F3C")
        n.place(x=250, y=380)

        p = Button(text="<--", command=left_arrow, bg="#16A085", font="verdana 10 bold", fg="#212F3C")
        p.place(x=170, y=380)


class Bisection(object):
    # Default Max Iterations = 50, Default Epsilon = 0.00001
    def __init__(self, formula_as_str, x1, x2, max_iterations=50, epsilon=0.00001):
        self.x1 = float(x1)
        self.x2 = float(x2)
        self.max_iterations = int(max_iterations)
        self.epsilon = float(epsilon)
        self.formula_as_str = formula_as_str
        self.__i = -1
        self.approximate_root, self.number_of_iterations, self.errors, self.time, self.precision,\
        self.values, self.limits = self.solve()

    def next1(self):
        self.__i = self.__i + 1
        if self.__i > self.limits.__len__():
            self.__i = self.limits.__len__()-1
        return self.limits[self.__i]

    def prev(self):
        self.__i = self.__i - 1
        if self.__i < 0:
            self.__i = 0
        return self.limits[self.__i]

    def solve(self):
        number_of_iterations = 0
        errors = []
        time = 0
        values = []
        error = 100
        limits = []
        if evaluate_equation(self.formula_as_str, self.x1) * evaluate_equation(self.formula_as_str, self.x2) > 0:
            print("No Root")
        for i in range(self.max_iterations):
            number_of_iterations = number_of_iterations+1
            mid = (self.x1 + self.x2) / 2
            values.append(mid)
            limit = Limits(self.x1, self.x2, mid)
            limits.append(limit)
            if i != 0:
                error = abs((mid - approximate_root) / mid)
                errors.append(error)
            approximate_root = mid

            test = evaluate_equation(self.formula_as_str, self.x1) * evaluate_equation(self.formula_as_str, mid)
            if test < 0:
                self.x2 = mid
            else:
                self.x1 = mid
            if test == 0 or error < self.epsilon:
                approximate_root = mid
                break

        precision = errors[-1]
        return approximate_root, number_of_iterations, errors, time, precision, values, limits



class Limits(object):
    def __init__(self, x1, x2, mid):
        self.points = [x1, x2]
        self.mid = mid

    def get(self):
        return self.points, self.mid



def right_arrow():
    limit = main.next1()
    point, mid = limit.get()
    plt.close('all')
    plt.figure(1)
    plt.title("Bisection Method")
    plt.xlabel("X")
    plt.ylabel("F(X)")
    plt.axvline(point[0])
    plt.axvline(point[1])
    plt.axvline(mid)
    x1 = np.linspace(0, 0.12)
    y1 = function(x1)
    plt.ylim(-0.0003, 0.0003)
    plt.plot(x1, y1, "r-*")
    plt.show(block=False)




def left_arrow():
    limit = main.prev()
    point, mid = limit.get()
    plt.close('all')
    plt.figure(1)
    plt.title("Bisection Method")
    plt.xlabel("X")
    plt.ylabel("F(X)")
    plt.axvline(point[0])
    plt.axvline(point[1])
    plt.axvline(mid)
    x1 = np.linspace(0, 0.12)
    y1 = function(x1)
    plt.ylim(-0.0003, 0.0003)
    plt.plot(x1, y1, "r-*")
    plt.show(block=False)


def function(x):
    return x ** 3 - 0.165 * x ** 2 + 3.993 * 10 ** -4




root = Tk()
b = Main(root)
root.bind("<Right>", right_arrow)
root.bind("<Left>", left_arrow)
root["bg"] = "#212F3C"
root.mainloop()
