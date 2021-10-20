from amuse.lab import *
from amuse.units import (units, constants)
import matplotlib.pyplot as plt
from amuse.community.mesa.interface import MESA
import numpy as np

# Constants of the Sun (maybe use the AMUSE constants)
z = 0.0134
TSun = 5778
LSun = 3.826e33
RSun = 696340e5
current_age_sun = 4.603e3 | units.Myr

evolving_age = 12e3 | units.Myr

# This is a testing age because 12 Gyr takes a long time
# evolving_age = 6e3 | units.Myr

stellar = MESA()

sun = Particles(1)
sun.mass = 1 | units.MSun

# We can just ignore these parameters, MESA will calculate them
# sun.radius = RSun | units.cm 
# sun.density = 1.41 | units.g / units.cm**3
# sun.temperature = TSun | units.K
# sun.luminosity = LSun | units.erg / units.s

stellar.particles.add_particles(sun)
stellar.parameters.metallicity = z

print(stellar.particles[0])

time_evolution = []
luminosity_evolution = []
radius_evolution = []
temperature_evolution = []
mass_evolution = []

while stellar.particles[0].age <= evolving_age:
    time_evolution.append(stellar.particles[0].age.value_in(units.Myr))
    luminosity_evolution.append(stellar.particles[0].luminosity.value_in(units.LSun) * LSun)
    radius_evolution.append(stellar.particles[0].radius.value_in(units.RSun) * RSun)
    temperature_evolution.append(stellar.particles[0].temperature.value_in(units.K))
    mass_evolution.append(stellar.particles[0].mass.value_in(units.MSun))
    
    print(stellar.particles[0].age.in_(units.Myr))
    
    stellar.evolve_model()
    
print(stellar.particles[0])

write_set_to_file(stellar.particles, "stellar_evolution_sun.amuse", "amuse", append_to_file=False)

stellar.stop()

time_evolution = np.array(time_evolution)
luminosity_evolution = np.array(luminosity_evolution)
radius_evolution = np.array(radius_evolution)
temperature_evolution = np.array(temperature_evolution)
mass_evolution = np.array(mass_evolution)

# plt.plot(time_evolution / 1000, luminosity_evolution / LSun, label="luminosity")
# plt.plot(time_evolution / 1000, radius_evolution / RSun, label="radius")
# plt.plot(time_evolution / 1000, temperature_evolution / TSun, label="temperature")
# plt.plot(time_evolution / 1000, mass_evolution / units.MSun.value_in(units.MSun), label="mass")
# plt.xlabel("Time [Gyr]")
# plt.ylabel("Ratio with current Sun")
# plt.legend(loc="upper left")
# plt.show()