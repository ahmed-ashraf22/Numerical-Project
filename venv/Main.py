# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 00:53:21 2019

@author: dell
"""

import _ssl
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from functools import partial
import parser


# TODO : adding trigonometry parsing
def evaluate_equation(formula, x):
    code = parser.expr(formula).compile()
    return eval(code)


# global variables
global_limits = []
i = -1


class Main:
    # GUI init.
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
        global global_limits
        formula_as_str = self.function_entry.get()
        max_iter = self.max_entry.get()
        x1 = self.x0_entry.get()
        x2 = self.x1_entry.get()
        eps = self.epsilon_entry.get()
        if self.current_method == "Bisection":
            method = Bisection(formula_as_str, x1, x2, max_iter, eps)
        elif self.current_method == "Newton-Raphson":
            method = NewtonRaphson(formula_as_str, x1, x2, max_iter, eps)
        elif self.current_method == "False-Position":
            method = FalsePosition(formula_as_str, x1, x2, max_iter, eps)
        elif self.current_method == "Fixed Point":
            method = FixedPoint(formula_as_str, x1, x2, max_iter, eps)
        elif self.current_method == "Secant":
            method = Secant(formula_as_str, x1, x2, max_iter, eps)
        else:
            method = BiergeVieta(formula_as_str, x1, x2, max_iter, eps)
        print(formula_as_str)
        result, number_of_iterations, errors, time, precision, values, global_limits = method.solve()
        print(result)
        print(number_of_iterations)
        print(errors)
        print(time)
        print(precision)
        print(values)
        print(global_limits)

        # TODO : use flexible plotting scales
        # Plotting
        plt.figure(1)
        plt.title(self.current_method)
        plt.xlabel("X")
        plt.ylabel("F(X)")
        x1 = np.linspace(0, 0.12)
        y1 = evaluate_equation(formula_as_str, x1)
        plt.ylim(-0.0003, 0.0003)
        plt.plot(x1, y1, "b-*")
        plt.show(block=False)

        iteration_label = Label(text="Iterations: ", font="verdana 10 bold", bg="#212F3C", pady=20,
                                fg="#16A085")

        iteration_label.place(x=50, y=360)
        n = Button(text="-->", command=self.right_arrow, bg="#16A085", font="verdana 10 bold", fg="#212F3C")
        n.place(x=250, y=380)

        p = Button(text="<--", command=self.left_arrow, bg="#16A085", font="verdana 10 bold", fg="#212F3C")
        p.place(x=170, y=380)

    def right_arrow(self):
        global i
        global global_limits
        i = i + 1
        if i >= len(global_limits):
            i = len(global_limits) - 1
        limit = global_limits[i]
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
        y1 = evaluate_equation(self.function_entry.get(), x1)
        plt.ylim(-0.0003, 0.0003)
        plt.plot(x1, y1, "r-*")
        plt.show(block=False)

    def left_arrow(self):
        global i
        i = i - 1
        if i < 0:
            i = 0
        limit = global_limits[i]
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
        y1 = evaluate_equation(self.function_entry.get(), x1)
        plt.ylim(-0.0003, 0.0003)
        plt.plot(x1, y1, "r-*")
        plt.show(block=False)


class Bisection(object):
    # Default Max Iterations = 50, Default Epsilon = 0.00001
    def __init__(self, formula_as_str, x1, x2, max_iterations=50, epsilon=0.00001):
        self.x1 = float(x1)
        self.x2 = float(x2)
        self.max_iterations = int(max_iterations)
        self.epsilon = float(epsilon)
        self.formula_as_str = formula_as_str

    def solve(self):
        number_of_iterations = 0
        errors = []
        time = 0
        values = []
        limits = []
        error = 100
        if evaluate_equation(self.formula_as_str, self.x1) * evaluate_equation(self.formula_as_str, self.x2) > 0:
            print("No Root")
        for i in range(self.max_iterations):
            number_of_iterations = number_of_iterations + 1
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
            elif test > 0:
                self.x1 = mid
            if test == 0 or error < self.epsilon:
                approximate_root = mid
                break

        precision = errors[-1]
        return approximate_root, number_of_iterations, errors, time, precision, values, limits


class Secant(object):
    # Default Max Iterations = 50, Default Epsilon = 0.00001
    def __init__(self, formula_as_str, x1, x2, max_iterations=50, epsilon=0.00001):
        self.x1 = float(x1)
        self.x2 = float(x2)
        self.max_iterations = int(max_iterations)
        self.epsilon = float(epsilon)
        self.formula_as_str = formula_as_str

    # def solve(self):


class NewtonRaphson(object):
    # Default Max Iterations = 50, Default Epsilon = 0.00001
    def __init__(self, formula_as_str, x1, x2, max_iterations=50, epsilon=0.00001):
        self.x1 = float(x1)
        self.x2 = float(x2)
        self.max_iterations = int(max_iterations)
        self.epsilon = float(epsilon)
        self.formula_as_str = formula_as_str

    # def solve(self):


class FalsePosition(object):
    # Default Max Iterations = 50, Default Epsilon = 0.00001
    def __init__(self, formula_as_str, x1, x2, max_iterations=50, epsilon=0.00001):
        self.x1 = float(x1)
        self.x2 = float(x2)
        self.max_iterations = int(max_iterations)
        self.epsilon = float(epsilon)
        self.formula_as_str = formula_as_str

    # def solve(self):


class FixedPoint(object):
    # Default Max Iterations = 50, Default Epsilon = 0.00001
    def __init__(self, formula_as_str, x1, x2, max_iterations=50, epsilon=0.00001):
        self.x1 = float(x1)
        self.x2 = float(x2)
        self.max_iterations = int(max_iterations)
        self.epsilon = float(epsilon)
        self.formula_as_str = formula_as_str

    # def solve(self):


class BiergeVieta(object):
    # Default Max Iterations = 50, Default Epsilon = 0.00001
    def __init__(self, formula_as_str, x1, x2, max_iterations=50, epsilon=0.00001):
        self.x1 = float(x1)
        self.x2 = float(x2)
        self.max_iterations = int(max_iterations)
        self.epsilon = float(epsilon)
        self.formula_as_str = formula_as_str

    # def solve(self):


class Limits(object):
    def __init__(self, x1, x2, mid):
        self.points = [x1, x2]
        self.mid = mid

    def get(self):
        return self.points, self.mid


# tkinter main GUI window
root = Tk()
b = Main(root)
root["bg"] = "#212F3C"
root.mainloop()
