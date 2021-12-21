from amuse.lab import *
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import ast

t_evolve = 12 # Gyr
t_end = 1 # yr
n = 100 # number of loops
z = 0.0134 # metallicity

au = 1.5e13 # cm
RSun = 696340e5 #cm

years_to_plot = 12 
timestep = 0.05
n_idx = int(years_to_plot / timestep)

times = np.arange(0, t_end * years_to_plot, timestep)
label_names = ["core", "gas", "earth_t0"]

# The csv file is otherwise too big to use
csv.field_size_limit(sys.maxsize)

# Make two dictionaries to save the coordinates in
x_coordinates = dict()
y_coordinates = dict()

with open("coordinates_t_end={}yr_n={}_z={}.csv".format(t_end, n, z)) as csvfile:
    coordinates = csv.reader(csvfile)

    # csv file: row[0]=name, row[1]=x, row[2]=y
    for row in coordinates:
        # The ast.literal_eval makes from a string list a list with floats
        x_coordinates[row[0]] = ast.literal_eval(row[1])
        y_coordinates[row[0]] = ast.literal_eval(row[2])

# Plots a grey line in the background to connect the scatter dots
plt.plot(np.array(x_coordinates["earth"][:n_idx])/RSun, np.array(y_coordinates["earth"][:n_idx])/RSun, linewidth=0.5, alpha=0.3, color="grey")

# Plots the first n_idx coordinates of the Earth with a color corresponding to a time
result = plt.scatter(np.array(x_coordinates["earth"][:n_idx])/RSun, np.array(y_coordinates["earth"][:n_idx])/RSun, label="earth", c=times, s=5)

# Plots the starting position of the Earth in red
earth = plt.scatter(np.array(x_coordinates["earth"][0])/RSun, np.array(y_coordinates["earth"][0])/RSun, color="red", label="earth_t0")

for i in range(years_to_plot):
    gravity_particles = read_set_from_file("gravity_particles_t_end={}yr_n={}_i={}_z={}.amuse".format(t_end, n, i, z), "amuse", append_to_file=False)
    hydro_particles = read_set_from_file("hydro_particles_t_end={}yr_n={}_i={}_z={}.amuse".format(t_end, n, i, z), "amuse", append_to_file=False)

    # Coordinates at the end of the run
    gas = plt.scatter(hydro_particles.x[1:].value_in(units.cm)/RSun, hydro_particles.y[1:].value_in(units.cm)/RSun, color="blue")
    core = plt.scatter(hydro_particles.x[0].value_in(units.cm)/RSun, hydro_particles.y[0].value_in(units.cm)/RSun, color="orange")

plt.colorbar(result, label="Age [yr]")
plt.xlabel("x [RSun]")
plt.ylabel("y [RSun]")
plt.legend(handles=[core, gas, earth], labels=label_names, loc="lower right")
plt.title("Coordinates for t_end={}yr, n={} and z={}".format(t_end, n, z))
plt.show()
# plt.savefig("animation/scatter_plot_t_end={}yr_n={}_i={}_z={}_same_scale.png".format(t_end, n, i, z))
plt.close()
