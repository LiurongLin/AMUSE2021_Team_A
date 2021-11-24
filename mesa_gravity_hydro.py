from amuse.lab import *
from amuse.units import (units, constants)
from amuse.couple import bridge
from amuse.units import quantities
from amuse.ext.orbital_elements import orbital_elements_from_binary
import matplotlib.pyplot as plt
import matplotlib.patches as patch
import numpy as np
from tqdm import tqdm
import sys
import csv
import timeit

# If you want to quickly check if it works: uncomment line 63 & 100 and comment line 62 & 99
# Also remember that if you ran it one time, that you delete the "mesa_gravity_hydro.amuse" file
# because otherwise you will get an error (because it cannot overwrite the file).

# Change parameter n and t_end (try n=5 and t_end=100yr again with new code for saving files)

# start run time
start = timeit.default_timer()

class friction:
    
    def __init__(self,hydro,particle):
        
        self.hydro = hydro
        self.particle = particle

    def get_gravity_at_point(self,eps,x,y,z):
        ##drag coefficient
        
        c_drag = 0.47
        
        result_ax = quantities.AdaptingVectorQuantity()
        result_ay = quantities.AdaptingVectorQuantity()
        result_az = quantities.AdaptingVectorQuantity()
        
        for i in range (2):
        
            hydro_density = self.hydro.get_hydro_state_at_point(self.particle[i].x,self.particle[i].y,self.particle[i].z,
                                                          self.particle[i].vx,self.particle[i].vy,self.particle[i].vz)[0]
            vx = self.particle[i].vx
            vy = self.particle[i].vy
            vz = self.particle[i].vz

            cross_section = np.pi*(self.particle[i].radius)**2

            ax = (0.5 * hydro_density * vx**2 * c_drag * cross_section)/self.particle[i].mass
            ay = (0.5 * hydro_density * vy**2 * c_drag * cross_section)/self.particle[i].mass
            az = (0.5 * hydro_density * vz**2 * c_drag * cross_section)/self.particle[i].mass
        
        
            result_ax.append(ax)
            result_ay.append(ay)
            result_az.append(az)
        
        return result_ax,result_ay,result_az

z = 0.0134
RSun = 696340e5 #cm
RRoche = 0.9*1.5e11 | units.m
# evolving_age = 12e3 | units.Myr
evolving_age = 1e3 | units.Myr
n = 1

sun = Particles(1)
sun.mass = 1 | units.MSun

system = Particles(2)

# Earth
earth = system[0]
earth.name = "Earth"
earth.mass = units.MEarth(1)
earth.radius = units.REarth(1) 
earth.position = np.array((1,0.0,0.0)) | units.au
earth.velocity = np.array((0.0,29780,0.0)) | units.ms

# Moon
moon = system[1]
moon.name = "Moon"
moon.mass = units.kg(7.342e22)
moon.radius = units.km(1737.4)
moon.position = units.km(np.array((149.5e6 + 384399,0.0,0.0)))
moon.velocity = ([0.0,1.022,0] | units.km/units.s) + earth.velocity   

converter_gravity = nbody_system.nbody_to_si(system.mass.sum(), earth.position.length())
gravity = Huayno(converter_gravity)
gravity.particles.add_particles(system)
gravity.parameters.timestep = 0.1 | units.yr

stellar = MESA()
stellar.particles.add_particle(sun)
stellar.parameters.metallicity = z

evol_sun = stellar.particles[0]
iterations = 0

luminosity_sun = []
temperature_sun = []

# while evol_sun.radius <= RRoche or (evol_sun.age > evolving_age and old_radius > evol_sun.radius):
while evol_sun.age <= evolving_age:
    # print(evol_sun.age.in_(units.Myr))

    luminosity_sun.append(evol_sun.luminosity.value_in(units.LSun))
    temperature_sun.append(evol_sun.temperature.value_in(units.K))

    stellar.evolve_model()

    old_radius = evol_sun.radius
    iterations += 1

    if iterations == 100:
        iterations = 0
        print("Radius sun =", evol_sun.radius.in_(units.RSun))
        print("Evolving age =", evol_sun.age.in_(units.Myr))    

print("Evolving age =", evol_sun.age.in_(units.Myr))    

# print current run time
current_time = timeit.default_timer()
print("Current run time =", int((current_time-start)/60), "min")

target_core_mass = 0.8 * evol_sun.mass
part_of_smaller_mass = 0.25
N_h = (evol_sun.mass - target_core_mass) / (part_of_smaller_mass * (1 | units.MEarth))
# N_h = (evol_sun.mass - target_core_mass) / (part_of_smaller_mass * moon.mass)

sph_model = convert_stellar_model_to_SPH(evol_sun,
                                         round(N_h),
                                         with_core_particle = True,
                                         target_core_mass = 0.8 * evol_sun.mass,
                                         do_store_composition = False,
                                         base_grid_options=dict(type="fcc"))

core = sph_model.core_particle.as_set()
gas = sph_model.gas_particles

print("Ngas =", len(gas), "Ncore =", core)
print("RCore =", core.radius.value_in(units.m)[0])

x_coordinates = dict()
y_coordinates = dict()
eccentricities = dict()
semi_major_axis = dict()

x_coordinates["core"] = []
x_coordinates["gas_last"] = []
x_coordinates["earth"] = []
x_coordinates["moon"] = []

y_coordinates["core"] = []
y_coordinates["gas_last"] = []
y_coordinates["earth"] = []
y_coordinates["moon"] = []

eccentricities["earth"] = []
eccentricities["moon"] = []

semi_major_axis["earth"] = []
semi_major_axis["moon"] = []

for i in range(n):

    converter_hydro = nbody_system.nbody_to_si(gas.mass.sum(), gas[-1].position.length())
    hydro = Fi(converter_hydro, mode="openmp")#, redirection="none")
    hydro.dm_particles.add_particle(core)
    hydro.gas_particles.add_particles(gas)
    # hydro.parameters.timestep = 1e-3 | units.yr

    gravity_hydro = bridge.Bridge()#use_threading=False)
    if hydro.get_hydro_state_at_point(gravity.particles[0].x, gravity.particles[0].y, gravity.particles[0].z,
                                      gravity.particles[0].vx, gravity.particles[0].vy, 
                                      gravity.particles[0].vz)[0].value_in(units.kg/(units.m**3)) == 0:
        gravity_hydro.add_system(gravity, (hydro,))
    else:
        gravity_hydro.add_system(gravity, (hydro, friction(hydro, gravity.particles)))
    gravity_hydro.timestep = 0.5 * gravity.parameters.timestep
    # gravity_hydro.timestep = 1e-3 | units.yr
    print("Gravity_hydro timestep =", gravity_hydro.timestep)

    t_end = 1 | units.yr
    model_time = 0 | units.yr
    time = np.arange(model_time.value_in(units.yr), t_end.value_in(units.yr), gravity_hydro.timestep.value_in(units.yr)) | units.yr
    for t in tqdm(time, desc="gravity_hydro"):
        x_coordinates["core"].append(core.x.value_in(units.cm)[0])
        x_coordinates["gas_last"].append(gas[-1].x.value_in(units.cm))
        x_coordinates["earth"].append(gravity.particles[0].x.value_in(units.cm))
        x_coordinates["moon"].append(gravity.particles[1].x.value_in(units.cm))
        
        y_coordinates["core"].append(core.y.value_in(units.cm)[0])
        y_coordinates["gas_last"].append(gas[-1].y.value_in(units.cm))
        y_coordinates["earth"].append(gravity.particles[0].y.value_in(units.cm))
        y_coordinates["moon"].append(gravity.particles[1].y.value_in(units.cm))

        ae = orbital_elements_from_binary([core, gravity.particles[0]], G=constants.G)[2:4]
        semi_major_axis["earth"] = ae[0].value_in(units.m)
        eccentricities["earth"] = ae[1]

        ae = orbital_elements_from_binary([gravity.particles[0], gravity.particles[1]], G=constants.G)[2:4]
        semi_major_axis["moon"] = ae[0].value_in(units.m)
        eccentricities["moon"] = ae[1]

        gravity_hydro.evolve_model(t)

    stellar.evolve_model(t_end)

    write_set_to_file(gravity_hydro.particles, "gravity_particles_t_end={}yr_n={}_i={}.amuse".format(t_end.value_in(units.yr), n, i), "amuse", append_to_file=False)
    write_set_to_file(hydro.particles, "hydro_particles_t_end={}yr_n={}_i={}.amuse".format(t_end.value_in(units.yr), n, i), "amuse", append_to_file=False)
    
    plt.scatter(np.array(gas.x.value_in(units.cm)) / RSun, np.array(gas.y.value_in(units.cm)) / RSun)
    plt.scatter(np.array(core.x.value_in(units.cm)) / RSun, np.array(core.y.value_in(units.cm)) / RSun, label="Sun")
    plt.scatter(gravity.particles[0].x.value_in(units.cm) / RSun, gravity.particles[0].y.value_in(units.cm) / RSun, label="Earth")
    plt.scatter(gravity.particles[1].x.value_in(units.cm) / RSun, gravity.particles[1].y.value_in(units.cm) / RSun, label="Moon")
    plt.xlabel("x [RSun]")
    plt.ylabel("y [RSun]")
    plt.legend(loc="upper left")
    plt.savefig("scatter_plot_system_t_end={}yr_n={}_i={}".format(t_end.value_in(units.yr), n, i))
    plt.close()

    hydro.stop()

    sph_model = convert_stellar_model_to_SPH(evol_sun,
                                            round(N_h),
                                            with_core_particle = True,
                                            target_core_mass = 0.8 * evol_sun.mass,
                                            do_store_composition = False,
                                            base_grid_options=dict(type="fcc"))

    core = sph_model.core_particle.as_set()
    gas = sph_model.gas_particles

data_file = open("coordinates_t_end={}yr_n={}.csv".format(t_end.value_in(units.yr), n), mode='w')
data_writer = csv.writer(data_file)
for (key, x), y in zip(x_coordinates.items(), y_coordinates.values()):
    data_writer.writerow([key, x, y])
data_file.close()

data_file = open("ae_t_end={}yr_n={}.csv".format(t_end.value_in(units.yr), n), mode='w')
data_writer = csv.writer(data_file)
for (key, a), e in zip(semi_major_axis.items(), eccentricities.values()):
    data_writer.writerow([key, a, e])
data_file.close()

data_file = open("temperature_luminosity_sun_t_evolve={}Myr.csv".format(evolving_age.value_in(units.Myr), n), mode='w')
data_writer = csv.writer(data_file)
for T, L in zip(temperature_sun, luminosity_sun):
    data_writer.writerow([key, T, L])
data_file.close()

stellar.stop()
gravity.stop()

# stop and print run time
stop = timeit.default_timer()
print("Time:", int((stop-start)/60), "min")
