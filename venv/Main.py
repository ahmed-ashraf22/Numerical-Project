# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 00:53:21 2019

@author: dell
"""

import _ssl
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np


class Main:
    def __init__(self, master):
        width = 800
        height = 400
        x = (master.winfo_screenwidth() // 2) - (width // 2)
        y = (master.winfo_screenheight() // 2) - (height // 2)
        master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        master.title('Numerical Methods')
        frame = Frame(master)
        frame.configure(background='black')

        label_1 = Label(master, text="Function: ", font="verdana 10 bold", bg="#212F3C", fg="#16A085")
        label_1.place(x=50, y=120)

        function_entry = Entry(master)
        function_entry.place(x=150, y=120, width=200)

        label_1 = Label(master, text="Method: ", font="verdana 10 bold", bg="#212F3C", fg="#16A085")
        label_1.place(x=50, y=170)

        label_2 = Label(master, text="Max. NO. Iterations: ", font="verdana 10 bold", bg="#212F3C", fg="#16A085")
        label_2.place(x=50, y=220)

        label_3 = Label(master, text="Epsilon: ", font="verdana 10 bold", bg="#212F3C", fg="#16A085")
        label_3.place(x=380, y=220)

        epsilon_entry = Entry(master)
        epsilon_entry.place(x=460, y=220, width=50)

        max_entry = Entry(master)
        max_entry.place(x=220, y=220, width=50)

        x0 = Label(master, text="X0: ", font="verdana 10 bold", bg="#212F3C", fg="#16A085")
        x0.place(x=50, y=270)

        x0_entry = Entry(master)
        x0_entry.place(x=100, y=270, width=50)

        x1 = Label(master, text="X1: ", font="verdana 10 bold", bg="#212F3C", fg="#16A085")
        x1.place(x=172, y=270)

        x1_entry = Entry(master)
        x1_entry.place(x=220, y=270, width=50)

        b = Button(master, text="Solve", command=self.solve, bg="#16A085", font="verdana 10 bold", fg="#212F3C")
        b.place(x=380, y=320)

        # Create a Tkinter variable
        tkvar = StringVar(master)

        # Dictionary with options
        choices = {'Bisection', 'False-Position', 'Fixed Point', 'Newton-Raphson', 'Secant', 'Bierge-Vieta'}
        tkvar.set('Bisection')  # set the default option

        popupMenu = OptionMenu(master, tkvar, *choices)
        popupMenu.place(x=150, y=165)
        popupMenu["bg"] = "#16A085"

        label = Label(master, text="#.# Numerical Methods #.#", font="verdana 20 bold", bg="#212F3C", pady=20,
                      fg="#16A085")
        label.place(x=200, y=10)

    def solve(self):
        method = Bisection(0.0, 0.11, 10, 0.000001)
        print(method.function(1))
        root = method.solve()
        print(root)
        # plt.figure(1)
        # plt.title("Bisection Method")
        # plt.xlabel("X")
        # plt.ylabel("Y")
        # plt.axvline(0.02)
        # x1 = linspace(0, 0.12)
        # y1 = self.function(x1)
        # plt.ylim(-0.0003, 0.0003)
        # plt.plot(x1, y1, "b-*")
        # plt.show()

        def f(t):
            return np.exp(-t) * np.cos(2 * np.pi * t)

        x1 = np.linspace(0.0, 5.0)
        x2 = np.linspace(0.0, 2.0)

        y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
        y2 = np.cos(2 * np.pi * x2)

        plt.subplot(10, 1, 1)
        plt.plot(x1, y1, 'o-')
        plt.title('Bisection Method')
        plt.ylabel('Iteration 1')

        plt.subplot(10, 1, 2)
        plt.plot(x2, y2, '.-')
        plt.xlabel('time (s)')
        plt.ylabel('Iteration 2')

        plt.subplot(10, 1, 3)
        plt.plot(x2, y2, '.-')
        plt.xlabel('time (s)')
        plt.ylabel('Iteration 3')

        plt.subplot(10, 1, 4)
        plt.plot(x2, y2, '.-')
        plt.xlabel('time (s)')
        plt.ylabel('Iteration 4')

        plt.subplot(10, 1, 5)
        plt.plot(x2, y2, '.-')
        plt.xlabel('time (s)')
        plt.ylabel('Iteration 4')

        plt.subplot(10, 1, 6)
        plt.plot(x2, y2, '.-')
        plt.xlabel('time (s)')
        plt.ylabel('Iteration 4')

        plt.subplot(10, 1, 7)
        plt.plot(x2, y2, '.-')
        plt.xlabel('time (s)')
        plt.ylabel('Iteration 4')

        plt.subplot(10, 1, 8)
        plt.plot(x2, y2, '.-')
        plt.xlabel('time (s)')
        plt.ylabel('Iteration 4')

        plt.subplot(10, 1, 9)
        plt.plot(x2, y2, '.-')
        plt.xlabel('time (s)')
        plt.ylabel('Iteration 4')

        plt.subplot(10, 1, 10)
        plt.plot(x2, y2, '.-')
        plt.xlabel('time (s)')
        plt.ylabel('Iteration 4')

        plt.show()

    def function(self, x):
        return x ** 3 - 0.165 * x ** 2 + 3.993 * 10 ** -4


class Bisection(object):
    # Default Max Iterations = 50, Default Epsilon = 0.00001
    def __init__(self, x1, x2, max_iterations, epsilon):
        self.x1 = x1
        self.x2 = x2
        self.max_iterations = max_iterations
        self.epsilon = epsilon

    def solve(self):
        number_of_iterations = 0
        errors = []
        time = 0
        precision = 0
        values = []
        error = 100
        if self.function(self.x1) * self.function(self.x2) > 0:
            print("No Root")
        for i in range(self.max_iterations):
            number_of_iterations = number_of_iterations+1
            mid = (self.x1 + self.x2) / 2
            if i != 0:
                error = abs((mid - root) / mid)
            root = mid

            test = self.function(self.x1) * self.function(mid)
            if test < 0:
                self.x2 = mid
            else:
                self.x1 = mid
            if test == 0 or error < self.epsilon:
                root = mid
                break
        return root

    def function(self, x):
        return x ** 3 - 0.165 * x ** 2 + 3.993 * 10 ** -4


class Limits(object):
    def __init__(self, x1, x2):
        self.points = [x1, x2]

    def get(self):
        return self.points




root = Tk()
b = Main(root)
root["bg"] = "#212F3C"
list1 = Limits(5.0, 5.2)
variables = list1.get()
print(variables[0])
root.mainloop()
