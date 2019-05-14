import re


n = 4
txt = "x-4r+x-4r=-5"
x = re.findall("(([+-])?([\d]*|[\d]*\.[\d]*)?([\w])+)|((=)(-)?([\d]*\.[\d]*))", txt)
print(x)

list_of_coefficients = []
list_of_variables = []
list_of_results = []
for i in range(n+1):
    t = 0
    if x[i][5] == "=":
        if x[i][6] == "-":
            t = float(x[i][7]) * -1
        else:
            t = float(x[i][7])
        list_of_results.append(t)
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
print(list_of_results)
