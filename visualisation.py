from amuse.lab import *
import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import ast

# First make a folder 'animation' in current folder, so the figures can be saved in it.
# Then you have to calculate the minimum xlimit and ylimit and maximum xlimit and ylimit
# You want to do this so every figure has the same shape. You can do this by uncommenting 
# the lines 70-76 and 83-86 and comment line 80. Now run the code. After filling in the 
# numbers in lines 67 & 68, you can comment 70-76 and 83-86 again and uncomment line 80.
# All resulting figures will be saved in the folder 'animation'.

xaxis = []
yaxis = []

t_end = 15
n = 15
z = 0.0134

au = 1.5e13 # cm
RSun = 696340e5 #cm

# with open("t_end={}yr_n={}_z={}/time_for_loop_t_end={}yr_n={}_z={}.csv".format(t_end, n, z, t_end, n, z)) as csvfile:
#     time_file = csv.reader(csvfile)
#     temperatures = ast.literal_eval(next(time_file)[1])

times = np.arange(0, 15*n, 0.05)
label_names = ["core", "gas", "earth"]

# The csv file is otherwise too big to use
csv.field_size_limit(sys.maxsize)

# Make two dictionaries to save the coordinates in
x_coordinates = dict()
y_coordinates = dict()

with open("t_end={}yr_n={}_z={}/coordinates_t_end={}yr_n={}_z={}.csv".format(t_end, n, z, t_end, n, z)) as csvfile:
    coordinates = csv.reader(csvfile)

    # csv file: row[0]=name, row[1]=x, row[2]=y
    for row in coordinates:
        # The ast.literal_eval makes from a string list a list with floats
        x_coordinates[row[0]] = ast.literal_eval(row[1])
        y_coordinates[row[0]] = ast.literal_eval(row[2])

result = plt.scatter(np.array(x_coordinates["earth"])/RSun, np.array(y_coordinates["earth"])/RSun, label="earth", c=times, s=2)

for i in range(n):
    gravity_particles = read_set_from_file("t_end={}yr_n={}_z={}/gravity_particles_t_end={}yr_n={}_i={}_z={}.amuse".format(t_end, n, z, t_end, n, i, z), "amuse", append_to_file=False)
    hydro_particles = read_set_from_file("t_end={}yr_n={}_z={}/hydro_particles_t_end={}yr_n={}_i={}_z={}.amuse".format(t_end, n, z, t_end, n, i, z), "amuse", append_to_file=False)

    # Coordinates at the end of the run
    core = plt.scatter(hydro_particles.x[1:].value_in(units.cm)/RSun, hydro_particles.y[1:].value_in(units.cm)/RSun, color="blue")
    gas = plt.scatter(hydro_particles.x[0].value_in(units.cm)/RSun, hydro_particles.y[0].value_in(units.cm)/RSun, color="orange")
    earth = plt.scatter(gravity_particles.x[0].value_in(units.cm)/RSun, gravity_particles.y[0].value_in(units.cm)/RSun, color="green")

    # Coordinates for every timestep
    # for x, y, lab in zip(list(x_coordinates.values()), list(y_coordinates.values()), labels):
        # plt.plot(np.array(x)/au, np.array(y)/au, label=lab)

# print(min(x_coordinates["earth"])/RSun)
# print(max(x_coordinates["earth"])/RSun)
# print(min(y_coordinates["earth"])/RSun)
# print(max(y_coordinates["earth"])/RSun)

plt.colorbar(result, label="Age [yr]")

plt.xlabel("x [RSun]")
plt.ylabel("y [RSun]")
plt.legend(handles=[core, gas, earth], labels=label_names, loc="lower left")

plt.xlim(-1024, 1277)
plt.ylim(-1254, 1161)

# axes = plt.gca()
# x1, x2 = axes.get_xlim()
# xaxis.append(x1)
# xaxis.append(x2)
# y1, y2 = axes.get_ylim()
# yaxis.append(y1)
# yaxis.append(y2)

plt.title("Coordinates for t_end={}yr, n={} and z={}".format(t_end, n, z))
plt.show()
# plt.savefig("animation/scatter_plot_t_end={}yr_n={}_i={}_z={}_same_scale.png".format(t_end, n, i, z))
plt.close()

# print(min(xaxis))
# print(max(xaxis))
# print(min(yaxis))
# print(max(yaxis))
