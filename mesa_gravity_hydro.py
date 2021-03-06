from amuse.lab import *
from amuse.units import (units, constants)
from amuse.couple import bridge
from amuse.units import quantities
from amuse.ext.orbital_elements import get_orbital_elements_from_arrays
import numpy as np
from tqdm import tqdm
import sys
import csv
import timeit

# start run time
start = timeit.default_timer()

class friction:
    
    def __init__(self, hydro, particle):
        
        self.hydro = hydro
        self.particle = particle

    def get_gravity_at_point(self):
        
        # drag coefficient for a spherical object
        c_drag = 0.47
        
        result_ax = quantities.AdaptingVectorQuantity()
        result_ay = quantities.AdaptingVectorQuantity()
        result_az = quantities.AdaptingVectorQuantity()
        
        # Change the number in the for loop if you want to calculate the friction for multiple objects
        for i in range (1):
            
            # Calculate the density at given position
            hydro_density = self.hydro.get_hydro_state_at_point(self.particle[i].x,self.particle[i].y,self.particle[i].z,
                                                          self.particle[i].vx,self.particle[i].vy,self.particle[i].vz)[0]
            
            # Save the velocity components
            vx = self.particle[i].vx
            vy = self.particle[i].vy
            vz = self.particle[i].vz

            # Calculate the cross section
            cross_section = np.pi*(self.particle[i].radius)**2

            # Check in which direction the velocity components are and then
            # calculate the acceleration by dividing the drag force by the mass
            if vx.value_in(units.ms) < 0:
                ax = (0.5 * hydro_density * vx**2 * c_drag * cross_section)/self.particle[i].mass
            if vx.value_in(units.ms) >= 0:
                ax = -(0.5 * hydro_density * vx**2 * c_drag * cross_section)/self.particle[i].mass     
            if vy.value_in(units.ms) < 0:
                ay = (0.5 * hydro_density * vy**2 * c_drag * cross_section)/self.particle[i].mass
            if vy.value_in(units.ms) >= 0:
                ay = -(0.5 * hydro_density * vy**2 * c_drag * cross_section)/self.particle[i].mass   
            if vz.value_in(units.ms) < 0:
                az = (0.5 * hydro_density * vz**2 * c_drag * cross_section)/self.particle[i].mass
            if vz.value_in(units.ms) >= 0:
                az = -(0.5 * hydro_density * vz**2 * c_drag * cross_section)/self.particle[i].mass
                
            result_ax.append(ax)
            result_ay.append(ay)
            result_az.append(az)
        
        return result_ax,result_ay,result_az

z = 0.0134 # metallicity
eta = 0.2 # mass loss rate efficiency
RSun = 696340e5 # cm
# RRoche = 0.5*1.5e11 | units.m
evolving_age = 12e3 | units.Myr
n = 100

sun = Particles(1)
sun.mass = 1 | units.MSun

stellar = MESA()
stellar.particles.add_particle(sun)
stellar.parameters.metallicity = z
# stellar.parameters.reimers_wind_efficiency = eta

evol_sun = stellar.particles[0]
iterations = 0

luminosity_sun = []
temperature_sun = []
mass_sun = []
radius_sun = []
time_sun = []

# while evol_sun.radius <= RRoche or (evol_sun.age > evolving_age and old_radius > evol_sun.radius):
while evol_sun.age <= evolving_age:

    # Save the Sun's parameters
    luminosity_sun.append(evol_sun.luminosity.value_in(units.LSun))
    temperature_sun.append(evol_sun.temperature.value_in(units.K))
    mass_sun.append(evol_sun.mass.value_in(units.MSun))
    radius_sun.append(evol_sun.radius.value_in(units.RSun))
    time_sun.append(evol_sun.age.value_in(units.Myr))

    stellar.evolve_model()

    old_radius = evol_sun.radius
    iterations += 1

    # Print radius and age every 100 iterations
    if iterations == 100:
        iterations = 0
        print("Radius sun =", evol_sun.radius.in_(units.RSun))
        print("Evolving age =", evol_sun.age.in_(units.Myr))    

print("Evolving age =", evol_sun.age.in_(units.Myr))    

# Save the Sun's parameters
data_file = open("temperature_luminosity_sun_t_evolve={}Myr_z={}_eta={}.csv".format(int(evol_sun.age.value_in(units.Myr)), z, eta), mode='w')
data_writer = csv.writer(data_file)
data_writer.writerow(["T [K]", temperature_sun])
data_writer.writerow(["L [LSun]", luminosity_sun])
data_writer.writerow(["M [MSun]", mass_sun])
data_writer.writerow(["R [RSun]", radius_sun])
data_writer.writerow(["Time [Myr]", time_sun])
data_file.close()

# Print current run time
current_time = timeit.default_timer()
print("Current run time =", int((current_time-start)/60), "min")

# Make the gravity particle
system = Particles(1)

# Earth
earth = system[0]
earth.name = "Earth"
earth.mass = units.MEarth(1)
earth.radius = units.REarth(1) 
earth.position = np.array((1,0.0,0.0)) | units.au
def relative_orbital_velocity(mass, distance):
    return ((constants.G*mass/distance).sqrt()).value_in(units.km/units.s)
vorb = relative_orbital_velocity(evol_sun.mass + earth.mass, earth.position.sum())
earth.velocity = np.array((0.0,1,0.0)) * vorb | units.km/units.s
print("v_earth =", earth.velocity)

converter_gravity = nbody_system.nbody_to_si(system.mass.sum(), earth.position.length())
gravity = Huayno(converter_gravity)
gravity.particles.add_particles(system)
gravity.parameters.timestep = 0.1 | units.yr

# Make the the core and gas particles
target_core_mass = 0.8 * evol_sun.mass
part_of_smaller_mass = 0.25
N_h = (evol_sun.mass - target_core_mass) / (part_of_smaller_mass * (1 | units.MEarth))

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
time_for_loop = dict()

x_coordinates["core"] = []
x_coordinates["gas_last"] = []
x_coordinates["earth"] = []

y_coordinates["core"] = []
y_coordinates["gas_last"] = []
y_coordinates["earth"] = []

eccentricities["earth"] = []
semi_major_axis["earth"] = []

mass_core = []
mass_gas = []

for i in range(n):
    time_for_loop[i] = []

    # Add the core and gas particles to the hydro code
    converter_hydro = nbody_system.nbody_to_si(gas.mass.sum(), gas[-1].position.length())
    hydro = Fi(converter_hydro, mode="openmp")
    hydro.dm_particles.add_particle(core)
    hydro.gas_particles.add_particles(gas)

    gravity_hydro = bridge.Bridge()

    # Check if friction should be taken into account (when density at Earth's position is nonzero)
    if hydro.get_hydro_state_at_point(gravity.particles[0].x, gravity.particles[0].y, gravity.particles[0].z,
                                      gravity.particles[0].vx, gravity.particles[0].vy, 
                                      gravity.particles[0].vz)[0].value_in(units.kg/(units.m**3)) == 0:
        gravity_hydro.add_system(gravity, (hydro,))
    else:
        gravity_hydro.add_system(gravity, (hydro, friction(hydro, gravity.particles)))
    gravity_hydro.timestep = 0.5 * gravity.parameters.timestep

    t_end = 1 | units.yr
    model_time = 0 | units.yr
    time = np.arange(model_time.value_in(units.yr), t_end.value_in(units.yr), gravity_hydro.timestep.value_in(units.yr)) | units.yr
    for t in tqdm(time, desc="gravity_hydro"):
        x_coordinates["core"].append(core.x.value_in(units.cm)[0])
        x_coordinates["gas_last"].append(gas[-1].x.value_in(units.cm))
        x_coordinates["earth"].append(gravity.particles[0].x.value_in(units.cm))
        
        y_coordinates["core"].append(core.y.value_in(units.cm)[0])
        y_coordinates["gas_last"].append(gas[-1].y.value_in(units.cm))
        y_coordinates["earth"].append(gravity.particles[0].y.value_in(units.cm))

        ae = get_orbital_elements_from_arrays(gravity.particles[0].position, gravity.particles[0].velocity, \
            (core.mass[0] + gas.mass.sum() + gravity.particles[0].mass), G=constants.G)[:2]
        semi_major_axis["earth"].append(ae[0][0].value_in(units.m))
        eccentricities["earth"].append(ae[1][0])

        mass_core.append(core.mass[0].value_in(units.MSun))
        mass_gas.append(gas.mass.sum().value_in(units.MSun))

        time_for_loop[i].append(t.value_in(units.yr))

        gravity_hydro.evolve_model(t)

    stellar.evolve_model(t_end)

    # Write the gravity and hydro particle sets to an amuse file
    write_set_to_file(gravity_hydro.particles, "gravity_particles_t_end={}yr_n={}_i={}_z={}.amuse".format(t_end.value_in(units.yr), n, i, z), "amuse", append_to_file=True)
    write_set_to_file(hydro.particles, "hydro_particles_t_end={}yr_n={}_i={}_z={}.amuse".format(t_end.value_in(units.yr), n, i, z), "amuse", append_to_file=True)
    
    hydro.stop()

    # Make new core and gas particles of the evolved model
    sph_model = convert_stellar_model_to_SPH(evol_sun,
                                            round(N_h),
                                            with_core_particle = True,
                                            target_core_mass = 0.8 * evol_sun.mass,
                                            do_store_composition = False,
                                            base_grid_options=dict(type="fcc"))

    core = sph_model.core_particle.as_set()
    gas = sph_model.gas_particles

# Write the saved dictionaries to a file
data_file = open("coordinates_t_end={}yr_n={}_z={}.csv".format(t_end.value_in(units.yr), n, z), mode='w')
data_writer = csv.writer(data_file)
for (key, x), y in zip(x_coordinates.items(), y_coordinates.values()):
    data_writer.writerow([key, x, y])
data_file.close()

data_file = open("ae_t_end={}yr_n={}_z={}.csv".format(t_end.value_in(units.yr), n, z), mode='w')
data_writer = csv.writer(data_file)
for (key, a), e in zip(semi_major_axis.items(), eccentricities.values()):
    data_writer.writerow([key, a, e])
data_file.close()

data_file = open("masses_core_gas_t_end={}yr_n={}_z={}.csv".format(t_end.value_in(units.yr), n, z), mode='w')
data_writer = csv.writer(data_file)
data_writer.writerow(["mass_core [MSun]", mass_core])
data_writer.writerow(["mass_gas [MSun]", mass_gas])
data_file.close()

data_file = open("time_for_loop_t_end={}yr_n={}_z={}.csv".format(t_end.value_in(units.yr), n, z), mode='w')
data_writer = csv.writer(data_file)
for key, tf in time_for_loop.items():
    data_writer.writerow([key, tf])
data_file.close()

stellar.stop()
gravity.stop()

# Stop and print run time
stop = timeit.default_timer()
print("Time:", int((stop-start)/60), "min")
