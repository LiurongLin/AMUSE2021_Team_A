from amuse.lab import *
import matplotlib.pyplot as plt
import numpy as np
import csv
import ast
import sys

# Will only work for the files that come from the new mesa_gravity_hydro.py

t_evolve = 12000.0
   
# The csv file is otherwise too big to use
csv.field_size_limit(sys.maxsize)

with open("temperature_luminosity_sun_t_evolve={}Myr.csv".format(t_evolve)) as csvfile:
    temp_lum = csv.reader(csvfile)
    temperatures = ast.literal_eval(next(temp_lum)[1])
    luminosities = ast.literal_eval(next(temp_lum)[1])

age = np.linspace(0, 12137, len(temperatures))

result = plt.scatter(temperatures, luminosities, c=age, s=0.3)
plt.colorbar(result, label="Age [Myr]")
plt.xlabel("Temperature [K]")
plt.ylabel(r"Luminosity [L$_\odot$]")
plt.gca().invert_xaxis()
plt.xscale('log')
plt.yscale('log')
plt.title("HR-diagram")
plt.show()
plt.close()
