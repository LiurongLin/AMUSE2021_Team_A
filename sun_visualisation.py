from amuse.lab import *
import matplotlib.pyplot as plt
import numpy as np
import csv
import ast
import sys

# Will only work for the files that come from the new mesa_gravity_hydro.py

t_evolve = 12136
t_end = 15
n = 15
z = 0.0134
   
# The csv file is otherwise too big to use
csv.field_size_limit(sys.maxsize)

with open("t_end={}yr_n={}_z={}/temperature_luminosity_sun_t_evolve={}Myr_z={}.csv".format(t_end, n, z, t_evolve, z)) as csvfile:
    temp_lum = csv.reader(csvfile)
    temperatures = ast.literal_eval(next(temp_lum)[1])
    luminosities = ast.literal_eval(next(temp_lum)[1])
    masses = ast.literal_eval(next(temp_lum)[1])
    radii = ast.literal_eval(next(temp_lum)[1])
    times = ast.literal_eval(next(temp_lum)[1])

# plt.plot(times, np.log10(luminosities), label="L")
# plt.plot(times, np.log10(temperatures), label="T")
plt.plot(times, masses, label="M")
# plt.plot(times, radii, label="R")
plt.xlabel("Time [Myr]")
plt.ylabel(r"M / M$_\odot$")
# plt.legend(loc="upper left")
plt.title("Mass of the Sun as a function of time")
plt.savefig("t_end={}yr_n={}_z={}/mass_t_end={}yr_n={}_z={}.png".format(t_end, n, z, t_end, n, z))
# plt.show()
plt.close()
