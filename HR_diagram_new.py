from amuse.lab import *
import matplotlib.pyplot as plt
import numpy as np
import csv
import ast
import sys

# Will only work for the files that come from the new mesa_gravity_hydro.py

t_evolve = 12136
t_end = 50
n = 10
z = 0.0142
   
# The csv file is otherwise too big to use
csv.field_size_limit(sys.maxsize)

with open("t_end={}yr_n={}_z={}/temperature_luminosity_sun_t_evolve={}Myr_z={}.csv".format(t_end, n, z, t_evolve, z)) as csvfile:
    temp_lum = csv.reader(csvfile)
    temperatures = ast.literal_eval(next(temp_lum)[1])
    luminosities = ast.literal_eval(next(temp_lum)[1])

age = np.linspace(0, 12137, len(temperatures))

# result = plt.scatter(temperatures, luminosities, s=0.3)#, c=age)
plt.plot(np.log10(temperatures), np.log10(luminosities))
# plt.colorbar(result, label="Age [Myr]")
plt.xlabel("log T [K]")
plt.ylabel(r"log(L / L$_\odot$)")
plt.gca().invert_xaxis()
# plt.xscale('log')
# plt.yscale('log')
plt.title("HR-diagram")
# plt.savefig("t_end={}yr_n={}_z={}/HR_diagram_t_end={}yr_n={}_z={}.png".format(t_end, n, z, t_end, n, z))
# plt.show()
plt.close()
