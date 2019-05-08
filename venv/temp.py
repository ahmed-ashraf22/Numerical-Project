from sympy import *


x= Symbol('x')

function = x**4 + 7*x**3 + 8

deriv= Derivative(function, x)
deriv.doit().subs({x: 4})

print(function.doit().subs({x: 4}))
print(deriv.doit().subs({x: 4}))