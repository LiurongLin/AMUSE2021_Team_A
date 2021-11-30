from amuse.lab import *
import matplotlib.pyplot as plt
import numpy as np
import csv
import ast
import sys

t_end = 2
n = 1

# The csv file is otherwise too big to use
csv.field_size_limit(sys.maxsize)

a = dict()
e = dict()
with open("ae_t_end={}yr_n={}.csv".format(t_end, n)) as csvfile:
    ae = csv.reader(csvfile)

    for row in ae:
        # The ast.literal_eval makes from a string list a list with floats
        a[row[0]] = ast.literal_eval(row[1])
        e[row[0]] = ast.literal_eval(row[2])

au = 1.5e11 # m

plt.plot(np.array(a["earth"])/au, e["earth"])
plt.xlabel("Semi-major axis [au]")
plt.ylabel("Eccentricity")
plt.title("Eccentricity as function of semi-major axis for the Earth")
plt.show()

plt.plot(np.array(a["moon"])/au, e["moon"])
plt.xlabel("Semi-major axis [au]")
plt.ylabel("Eccentricity")
plt.title("Eccentricity as function of semi-major axis for the Moon")
plt.show()