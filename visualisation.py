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

t_end = 50
n = 5

for i in range(n):
    gravity_particles = read_set_from_file("good_files/gravity_particles_t_end={}yr_n={}_i={}.amuse".format(t_end, n, i), "amuse", append_to_file=False)
    hydro_particles = read_set_from_file("good_files/hydro_particles_t_end={}yr_n={}_i={}.amuse".format(t_end, n, i), "amuse", append_to_file=False)

    # print("Number of gravity particles =", len(gravity_particles))
    # print("Number of hydro particles (including the core particle) =", len(hydro_particles))

    # # The csv file is otherwise too big to use
    # csv.field_size_limit(sys.maxsize)

    # # Make two dictionaries to save the coordinates in
    # x_coordinates = dict()
    # y_coordinates = dict()

    # with open("coordinates_t_end=100yr_n=5.csv") as csvfile:
    #     coordinates = csv.reader(csvfile)

    #     # csv file: row[0]=name, row[1]=x, row[2]=y
    #     for row in coordinates:
    #         # The ast.literal_eval makes from a string list a list with floats
    #         x_coordinates[row[0]] = ast.literal_eval(row[1])
    #         y_coordinates[row[0]] = ast.literal_eval(row[2])

    au = 1.5e13 # cm
    RSun = 696340e5 #cm

    # Core, gas, earth, moon
    # labels = list(x_coordinates.keys())
    labels = ["core", "gas", "earth", "moon"]

    # Coordinates at the end of the run
    plt.scatter(hydro_particles.x[1:].value_in(units.cm)/RSun, hydro_particles.y[1:].value_in(units.cm)/RSun, label="gas")
    plt.scatter(hydro_particles.x[0].value_in(units.cm)/RSun, hydro_particles.y[0].value_in(units.cm)/RSun, label=labels[0])
    plt.scatter(gravity_particles.x[0].value_in(units.cm)/RSun, gravity_particles.y[0].value_in(units.cm)/RSun, label=labels[2])
    plt.scatter(gravity_particles.x[1].value_in(units.cm)/RSun, gravity_particles.y[1].value_in(units.cm)/RSun, label=labels[3])

    # # Coordinates for every timestep
    # for x, y, lab in zip(list(x_coordinates.values()), list(y_coordinates.values()), labels):
    #     plt.plot(np.array(x)/au, np.array(y)/au, label=lab)

    plt.xlabel("x [RSun]")
    plt.ylabel("y [RSun]")
    plt.legend(loc="upper left")

    # plt.xlim(-582, 767)
    # plt.ylim(-291, 1308)
    plt.xlim(-660, 675)
    plt.ylim(-646, 534)

    # axes = plt.gca()
    # x1, x2 = axes.get_xlim()
    # xaxis.append(x1)
    # xaxis.append(x2)
    # y1, y2 = axes.get_ylim()
    # yaxis.append(y1)
    # yaxis.append(y2)

    plt.title("Coordinates for t_end={}yr and n={} (i={})".format(t_end, n, i))
    # plt.show()
    plt.savefig("animation/scatter_plot_t_end={}yr_n={}_i={}.png".format(t_end, n, i))
    plt.close()

# print(min(xaxis))
# print(max(xaxis))
# print(min(yaxis))
# print(max(yaxis))