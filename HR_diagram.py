import matplotlib.pyplot as plt
import numpy as np
import csv
import ast
import sys

# Will only work for the files that come from the new mesa_gravity_hydro.py

t_evolve = 12000 # Myr
t_end = 1 # yr
n = 100 # number of loops
z = 0.0134 # metallicity
eta = 0.2 # mass loss rate efficiency
   
# The csv file is otherwise too big to use
csv.field_size_limit(sys.maxsize)

with open("t_evolve=12Gyr_t_end=1_n=100_diff_v/temperature_luminosity_sun_t_evolve={}Myr_z={}_eta={}.csv".format(t_evolve, z, eta)) as csvfile:
    temp_lum = csv.reader(csvfile)
    temperatures = ast.literal_eval(next(temp_lum)[1])
    luminosities = ast.literal_eval(next(temp_lum)[1])
    masses = ast.literal_eval(next(temp_lum)[1])
    radii = ast.literal_eval(next(temp_lum)[1])
    times = ast.literal_eval(next(temp_lum)[1])

result = plt.scatter(np.log10(temperatures), np.log10(luminosities), s=2, c=times)

# Plots the position in the diagram of the current Sun
plt.scatter(3.76077, 0, color="red", s=10, label="Sun now")

plt.colorbar(result, label="Age [Myr]")
plt.xlabel("log T [K]")
plt.ylabel(r"log(L / L$_\odot$)")
plt.gca().invert_xaxis()
plt.title("HR-diagram")
plt.legend(loc="upper left")
# plt.savefig("t_end={}yr_n={}_z={}/HR_diagram_new_t_t_end={}yr_n={}_z={}.png".format(t_end, n, z, t_end, n, z))
plt.show()
plt.close()
