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
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from matplotlib.ticker import NullFormatter


# TODO : adding trigonometry parsing
def evaluate_equation(formula, x):
    code = parser.expr(formula).compile()
    return eval(code)


# global variables
global_limits = []
errors = []
i = -1


class Main:
    # GUI init.
    def __init__(self, master):
        global i
        global global_limits
        global errors
        self.current_method = "Bisection"
        width = 800
        height = 700
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
        choices = {'Bisection', 'False-Position', 'Fixed Point', 'Newton-Raphson', 'Secant', 'Birge-Vieta'}
        tkvar.set('Bisection')  # set the default option

        self.popupMenu = OptionMenu(master, tkvar, *choices, command=self.method_to_use)
        self.popupMenu.place(x=150, y=165)
        self.popupMenu["bg"] = "#16A085"

        label = Label(master, text="#.# Numerical Methods #.#", font="verdana 20 bold", bg="#212F3C", pady=20,
                      fg="#16A085")
        label.place(x=200, y=0)

        label = Label(master, text="Read from file (Insert file name) :", font="verdana 10 bold", bg="#212F3C", pady=20,
                      fg="#16A085")
        label.place(x=50, y=50)

        label = Label(master, text="(OR)", font="verdana 10 bold", bg="#212F3C", pady=20,
                      fg="#16A085")
        label.place(x=0, y=70)

        self.file_entry = Entry(master)
        self.file_entry.place(x=320, y=70, width=100)

        self.method = BisectionAndFalsePosition(True, "", 0, 0, 0, 0)
        self.result = 0

    def method_to_use(self, value):
        self.current_method = value

    def solve(self):
        global i
        global global_limits
        global errors
        file_mode = True
        i = -1
        errors = []
        self.formula_as_str = ""
        max_iter = 50
        x1 = ""
        x2 = ""
        eps = 0.00001
        if not file_mode:
            self.formula_as_str = self.function_entry.get()
            max_iter = self.max_entry.get()
            x1 = self.x0_entry.get()
            x2 = self.x1_entry.get()
            eps = self.epsilon_entry.get()
        # Reading from file
        if file_mode:
            file_name = self.file_entry.get()
            file = open(file_name, "r+")
            formula_as_str_list = file.readline().splitlines()
            self.formula_as_str = formula_as_str_list[0]
            current_method_list = file.readline().splitlines()
            self.current_method = current_method_list[0]
            x = file.readline()
            x = x.split()
            float_numbers = []
            for item in x:
                float_numbers.append(float(item))
            x1 = float_numbers[0]
            x2 = float_numbers[1]

        if self.current_method == "Bisection":
            self.method = BisectionAndFalsePosition(True, self.formula_as_str, x1, x2, max_iter, eps)
        elif self.current_method == "Newton-Raphson":
            self.method = NewtonRaphson(self.formula_as_str, x1, max_iter, eps)
        elif self.current_method == "False-Position":
            self.method = BisectionAndFalsePosition(False, self.formula_as_str, x1, x2, max_iter, eps)
        elif self.current_method == "Fixed Point":
            self.method = FixedPoint(self.formula_as_str, x1, max_iter, eps)
        elif self.current_method == "Secant":
            self.method = Secant(self.formula_as_str, x1, x2, max_iter, eps)
        else:
            self.method = BirgeVieta(self.formula_as_str, x1, x2, max_iter, eps)
        print(self.formula_as_str)
        if (self.current_method == 'Birge-Vieta'):
            self.method.solve()
            return
        self.result, number_of_iterations, errors, time, precision, values, global_limits = self.method.solve()
        print(self.result)
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
        y1 = evaluate_equation(self.formula_as_str, x1)
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

        root_label_title = Label(text="Approximated Root: ", font="verdana 10 bold", bg="#212F3C",
                                 pady=20, fg="#16A085")
        root_label_title.place(x=50, y=410)

        root_label = Label(text=self.result, font="verdana 10 bold", bg="#212F3C", pady=20,
                           fg="#F5FFFA")
        root_label.place(x=220, y=410)

        number_of_iterations_label_title = Label(text="NO. Iterations: ", font="verdana 10 bold",
                                                 bg="#212F3C", pady=20, fg="#16A085")
        number_of_iterations_label_title.place(x=50, y=460)

        number_of_iterations_label = Label(text=number_of_iterations, font="verdana 10 bold",
                                           bg="#212F3C", pady=20, fg="#F5FFFA")
        number_of_iterations_label.place(x=220, y=460)

        precision_label_title = Label(text="Precision: ", font="verdana 10 bold", bg="#212F3C",
                                      pady=20, fg="#16A085")
        precision_label_title.place(x=50, y=510)

        precision_label = Label(text=precision, font="verdana 10 bold", bg="#212F3C",
                                pady=20, fg="#F5FFFA")
        precision_label.place(x=220, y=510)

        time_label_title = Label(text="Time: ", font="verdana 10 bold", bg="#212F3C",
                                 pady=20, fg="#16A085")
        time_label_title.place(x=50, y=560)

        time_label = Label(text=time, font="verdana 10 bold", bg="#212F3C", pady=20, fg="#F5FFFA")
        time_label.place(x=220, y=560)

    def right_arrow(self):
        global i
        global global_limits
        global errors
        i = i + 1
        if i >= len(global_limits):
            i = len(global_limits) - 1
        limit = global_limits[i]
        point, mid = limit.get()
        if (self.current_method == "Bisection") | (self.current_method == "False-Position"):
            self.method.plot(point, mid, self.formula_as_str)
        elif self.current_method == "Newton-Raphson":
            self.method.plot(point, self.formula_as_str)
        elif self.current_method == "Fixed Point":
            self.method.plot(point, self.formula_as_str)
        elif self.current_method == "Secant":
            self.method.plot(point, mid, self.formula_as_str)
        elif self.current_method == "Fixed Point":
            self.method.plot(point[1], self.formula_as_str)

    def left_arrow(self):
        global i
        global global_limits
        global errors
        i = i - 1
        if i < 0:
            i = 0
        limit = global_limits[i]
        point, mid = limit.get()
        if (self.current_method == "Bisection") | (self.current_method == "False-Position"):
            self.method.plot(point, mid, self.formula_as_str)
        elif self.current_method == "Newton-Raphson":
            self.method.plot(point, self.formula_as_str)
        elif self.current_method == "Secant":
            self.method.plot(point, mid, self.formula_as_str)
        elif self.current_method == "Fixed Point":
            self.method.plot(point[1], self.formula_as_str)


class Secant(object):
    # Default Max Iterations = 50, Default Epsilon = 0.00001
    def __init__(self, formula_as_str, x1, x2, max_iterations=50, epsilon=0.00001):
        self.x1 = float(x1)
        self.x2 = float(x2)
        self.max_iterations = int(max_iterations)
        self.epsilon = float(epsilon)
        self.formula_as_str = formula_as_str

    def solve(self):
        # x ** 2 - 2 (Test)
        global errors
        number_of_iterations = 0
        time = 0
        values = []
        limits = []
        error = 100
        x0 = self.x1
        x1 = self.x2
        for i1 in range(self.max_iterations):
            number_of_iterations = number_of_iterations + 1
            x2 = x1 - ((evaluate_equation(self.formula_as_str, x1) * (x1 - x0)) /
                       (evaluate_equation(self.formula_as_str, x1) - evaluate_equation(self.formula_as_str, x0)))
            values.append(x2)
            if i1 != 0:
                error = abs((x2 - x1) / x2)
                errors.append(error)
            if error < self.epsilon:
                approximate_root = x2
                break
            limit = Limits(x0, x1, x2)
            limits.append(limit)
            x0 = x1
            x1 = x2
        precision = errors[-1]
        return approximate_root, number_of_iterations, errors, time, precision, values, limits

    def plot(self, point, x2, formula_as_str):
        global i
        global errors
        x_axis = [point[0], point[1], x2]
        y_axis = [evaluate_equation(formula_as_str, point[0]), evaluate_equation(formula_as_str, point[1]), 0]
        plt.close('all')
        plt.figure(1)
        if i == 0:
            plt.title("Iteration " + str(i + 1))
        else:
            plt.title("Iteration " + str(i + 1) + "   Error: " + str(errors[i - 1]))
        plt.xlabel("X = " + str(point[1]))
        plt.ylabel("F(X)")
        plt.axvline(point[0])
        plt.axvline(point[1])
        plt.axvline(x2)
        space = ((point[1] - point[0]) * 0.5)
        x1 = np.linspace(point[0] - space, point[1] + space)
        y1 = evaluate_equation(formula_as_str, x1)
        plt.plot(x1, y1, "r-")
        plt.plot(x_axis, y_axis, 1, "g")
        plt.show(block=False)


class NewtonRaphson(object):
    # Default Max Iterations = 50, Default Epsilon = 0.00001
    def __init__(self, formula_as_str, x1, max_iterations=50, epsilon=0.00001):
        self.x1 = float(x1)
        self.max_iterations = int(max_iterations)
        self.epsilon = float(epsilon)
        self.formula_as_str = formula_as_str

    def solve(self):
        global errors
        number_of_iterations = 0
        time = 0
        values = []
        limits = []
        error = 100
        x = Symbol('x')
        f = parse_expr(self.formula_as_str)
        f_prime = Derivative(f, x)
        x0 = self.x1
        for i1 in range(self.max_iterations):
            number_of_iterations = number_of_iterations + 1
            x1 = x0 - (f.doit().subs({x: x0}) / f_prime.doit().subs({x: x0}))
            x1 = float(x1)
            values.append(x1)
            if i1 != 0:
                error = abs((x1 - x0) / x1)
                errors.append(error)
            if error < self.epsilon:
                approximate_root = x1
                break
            limit = Limits(x0, x1, 0)
            limits.append(limit)
            x0 = x1
        precision = errors[-1]
        return approximate_root, number_of_iterations, errors, time, precision, values, limits

    def plot(self, point, formula_as_str):
        global i
        global errors
        first_tangent_point = [point[0], point[1]]
        second_tangent_point = [evaluate_equation(formula_as_str, point[0]),
                                evaluate_equation(formula_as_str, point[1])]
        plt.close('all')
        plt.figure(1)
        if i == 0:
            plt.title("Iteration " + str(i + 1))
        else:
            plt.title("Iteration " + str(i + 1) + "   Error: " + str(errors[i - 1]))
        plt.xlabel("X = " + str(point[1]))
        plt.ylabel("F(X)")
        plt.axvline(point[0])
        plt.axvline(point[1])
        space = ((point[1] - point[0]) * 0.5)
        x1 = np.linspace(point[0] - space, point[1] + space)
        y1 = evaluate_equation(formula_as_str, x1)
        plt.plot(x1, y1, "r-")
        plt.plot(first_tangent_point, second_tangent_point, 1, "g^")
        plt.show(block=False)


class BisectionAndFalsePosition(object):
    # Default Max Iterations = 50, Default Epsilon = 0.00001
    def __init__(self, bisection, formula_as_str, x1, x2, max_iterations=50, epsilon=0.00001):
        self.x1 = float(x1)
        self.x2 = float(x2)
        self.max_iterations = int(max_iterations)
        self.epsilon = float(epsilon)
        self.formula_as_str = formula_as_str
        self.bisection = bisection

    def solve(self):
        global errors
        number_of_iterations = 0
        time = 0
        values = []
        limits = []
        error = 100
        fl = evaluate_equation(self.formula_as_str, self.x1)
        fu = evaluate_equation(self.formula_as_str, self.x2)
        if fl * fu > 0:
            print("No Root")
        for i1 in range(self.max_iterations):
            fl = evaluate_equation(self.formula_as_str, self.x1)
            fu = evaluate_equation(self.formula_as_str, self.x2)
            number_of_iterations = number_of_iterations + 1
            if not self.bisection:
                mid = (self.x1 * fu - self.x2 * fl) / (fu - fl)
            else:
                mid = (self.x1 + self.x2) / 2
            values.append(mid)
            limit = Limits(self.x1, self.x2, mid)
            limits.append(limit)
            if i1 != 0:
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

    def plot(self, point, mid, formula_as_str):
        global i
        global errors
        plt.close('all')
        plt.figure(1)
        if i == 0:
            plt.title("Iteration " + str(i + 1))
        else:
            plt.title("Iteration " + str(i + 1) + "   Error: " + str(errors[i - 1]))
        plt.xlabel("X = " + str(mid))
        plt.ylabel("F(X)")
        plt.axvline(point[0])
        plt.axvline(point[1])
        plt.axvline(mid)
        space = ((point[1] - point[0]) * 0.5)
        x1 = np.linspace(point[0] - space, point[1] + space)
        y1 = evaluate_equation(formula_as_str, x1)
        plt.plot(x1, y1, "r-*")
        if not self.bisection:
            first_tangent_point = [point[0], point[1]]
            second_tangent_point = [evaluate_equation(formula_as_str, point[0]),
                                    evaluate_equation(formula_as_str, point[1])]
            plt.plot(first_tangent_point, second_tangent_point, 1, "g^")
        plt.show(block=False)


class FixedPoint(object):
    # Default Max Iterations = 50, Default Epsilon = 0.00001
    def __init__(self, formula_as_str, x1, max_iterations=50, epsilon=0.00001):
        self.x1 = float(x1)
        self.max_iterations = int(max_iterations)
        self.epsilon = float(epsilon)
        self.formula_as_str = formula_as_str
        self.x = Symbol('x')
        self.expression = parse_expr(self.formula_as_str + "- x")

    def solve(self):
        global errors
        number_of_iterations = 0
        time = 0
        values = []
        limits = []
        error = 100
        x0 = self.x1
        x = Symbol('x')
        coeff = Poly(self.formula_as_str, x).all_coeffs()
        coeff = coeff[-2]
        self.formula_as_str = self.formula_as_str + "-" + str(coeff) + "*x"
        div = -float(1 / coeff)
        for i1 in range(self.max_iterations):
            number_of_iterations = number_of_iterations + 1
            x1 = evaluate_equation(self.formula_as_str, x0) * div
            values.append(x1)
            approximate_root = x1
            if i1 != 0:
                error = abs((x1 - x0) / x1)
                errors.append(error)
            if error < self.epsilon:
                break
            limit = Limits(x0, x1, 0)
            limits.append(limit)
            x0 = x1
        precision = errors[-1]
        return approximate_root, number_of_iterations, errors, time, precision, values, limits

    def plot(self, a_root, formula_as_str):
        plt.close('all')
        plt.figure(1)
        plt.title("Fixed Point")
        plt.xlabel("X = " + str(a_root))
        plt.ylabel("F(X)")
        plt.axvline(a_root)
        x1 = np.linspace(0, 6)
        x2 = np.linspace(0, 6)
        y2 = evaluate_equation("x", x2)
        y1 = evaluate_equation(formula_as_str, x1)
        plt.plot(x1, y1, "r-*")
        plt.plot(x2, y2, "r-*")
        plt.show(block=False)


class BirgeVieta(object):
    # Default Max Iterations = 50, Default Epsilon = 0.00001
    def __init__(self, formula_as_str, x1, x2, max_iterations=50, epsilon=0.00001):
        self.x1 = float(x1)
        self.x2 = float(x2)
        self.max_iterations = int(max_iterations)
        self.epsilon = float(epsilon)
        self.formula_as_str = formula_as_str
        x = Symbol('x')
        self.coeff = Poly(formula_as_str, x).all_coeffs()
        self.deg = degree(parse_expr(formula_as_str), gen=x)
        self.coeff = [float(i) for i in self.coeff]

    def solve(self):
        sol = [self.x1]
        iterationRows = []
        errors = []
        roots = []
        time = 0
        if self.deg <= 1:
            return
        for i in range(self.max_iterations):
            b = [self.coeff[0]]
            for j in range(len(self.coeff) - 1):
                b.append((self.x1 * b[j]) + self.coeff[j + 1])
            c = [self.coeff[0]]
            for j in range(len(self.coeff) - 2):
                c.append((self.x1 * c[j]) + self.coeff[j + 1])
            self.x1 -= b[len(b) - 1] / c[len(c) - 1]
            sol.append(self.x1)
            if abs(1 - sol[len(sol) - 2] / self.x1) <= self.epsilon:
                break

        x_old = None
        for i in range(len(sol)):
            if x_old != None:
                ea = abs(sol[i] - x_old)
                ea_rel = abs(sol[i] - x_old) / max(abs(x_old), abs(sol[i]))
            else:
                ea = "-"
            iterationRows.append([i + 1, sol[i], evaluate_equation(self.formula_as_str, sol[i]), ea])
            errors.append((i + 1, ea))
            roots.append((i + 1, sol[i]))
            x_old = sol[i]

        table = BirgeVietaTable("Birge-Vieta", ['Step', 'xi', 'f(xi)', 'Abs. Error'], iterationRows)

        file = open("birge_vieta.txt", "w+")
        file.write(table.get_as_str())
        file.close()


class BirgeVietaTable(object):
    def __init__(self, title, header, data):
        self.header = header
        self.data = data
        self.title = title

    def get_as_str(self):
        string = "Table Title: " + str(self.title) + "\n" + str(self.header) + "\n"
        for row in self.data:
            string += str(row) + "\n"
        return string


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
