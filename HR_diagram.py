from amuse.lab import *
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

t_evolve = 12000.0
   
# The csv file is otherwise too big to use
csv.field_size_limit(sys.maxsize)

temperatures = []
luminosities = []

with open("temperature_luminosity_sun_t_evolve={}Myr.csv".format(t_evolve)) as csvfile:
    temp_lum = csv.reader(csvfile)

    for row in temp_lum:
        temperatures.append(float(row[1]))
        luminosities.append(float(row[2]))

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
