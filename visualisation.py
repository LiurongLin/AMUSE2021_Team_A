from amuse.lab import *
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import ast

gravity_particles = read_set_from_file("gravity_particles_t_end=100yr_n=5.amuse", "amuse", append_to_file=False)
hydro_particles = read_set_from_file("hydro_particles_t_end=100yr_n=5.amuse", "amuse", append_to_file=False)

print("Number of gravity particles =", len(gravity_particles))
print("Number of hydro particles (including the core particle) =", len(hydro_particles))

# The csv file is otherwise too big to use
csv.field_size_limit(sys.maxsize)

# Make two dictionaries to save the coordinates in
x_coordinates = dict()
y_coordinates = dict()

with open("coordinates_t_end=100yr_n=5.csv") as csvfile:
    coordinates = csv.reader(csvfile)

    # csv file: row[0]=name, row[1]=x, row[2]=y
    for row in coordinates:
        # The ast.literal_eval makes from a string list a list with floats
        x_coordinates[row[0]] = ast.literal_eval(row[1])
        y_coordinates[row[0]] = ast.literal_eval(row[2])

au = 1.5e13 # cm
RSun = 696340e5 #cm

# Core, gas, earth, moon
labels = list(x_coordinates.keys())

# Coordinates at the end of the run
plt.scatter(hydro_particles.x[1:].value_in(units.cm), hydro_particles.y[1:].value_in(units.cm), label="gas")
plt.scatter(hydro_particles.x[0].value_in(units.cm), hydro_particles.y[0].value_in(units.cm), label=labels[0])
plt.scatter(gravity_particles.x[0].value_in(units.cm), gravity_particles.y[0].value_in(units.cm), label=labels[2])
plt.scatter(gravity_particles.x[1].value_in(units.cm), gravity_particles.y[1].value_in(units.cm), label=labels[3])

# # Coordinates for every timestep
# for x, y, lab in zip(list(x_coordinates.values()), list(y_coordinates.values()), labels):
#     plt.plot(np.array(x)/au, np.array(y)/au, label=lab)

plt.xlabel("x [au]")
plt.ylabel("y [au]")
plt.legend(loc="upper left")
plt.show()
