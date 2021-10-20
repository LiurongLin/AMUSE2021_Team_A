# from astropy.constants import M_earth
from amuse.ext.star_to_sph import convert_stellar_model_to_SPH
from amuse.lab import *
from amuse.plot import sph_particles_plot
from amuse.units import (units, constants)
import matplotlib.pyplot as plt
import matplotlib.patches as patch
from amuse.community.mesa.interface import MESA
import numpy as np
from tqdm import tqdm
import sys

z = 0.0134
RSun = 696340e5

evolving_age = 12e3 | units.Myr
# evolving_age = 4e3 | units.Myr

stellar = MESA()

sun = Particles(1)
sun.mass = 1 | units.MSun

stellar.particles.add_particle(sun)
stellar.parameters.metallicity = z

evol_sun = stellar.particles[0]

while evol_sun.age <= evolving_age:
    
    print(evol_sun.age.in_(units.Myr))
    
    stellar.evolve_model()
    
target_core_mass = evol_sun.core_mass
part_of_smaller_mass = 0.25
N_h = (evol_sun.mass - target_core_mass) / (part_of_smaller_mass * (1 | units.MEarth))

sph_model = convert_stellar_model_to_SPH(evol_sun,
                                         round(N_h),
                                         with_core_particle = True,
                                         target_core_mass = target_core_mass,
                                         do_store_composition = False,
                                         base_grid_options=dict(type="fcc"))

core_particle = sph_model.core_particle.as_set()
gas_particles = sph_model.gas_particles

print("Ngas=", len(gas_particles), "Ncore=", core_particle)

write_set_to_file(core_particle, "core_particle.amuse", "amuse", append_to_file=False)
write_set_to_file(gas_particles, "gas_particles.amuse", "amuse", append_to_file=False)

stellar.stop()

print("RCore=", core_particle.radius.value_in(units.m)[0])

fig, ax = plt.subplots(figsize=(6, 6))
plt.scatter(np.array(gas_particles.x.value_in(units.cm)) / RSun, np.array(gas_particles.y.value_in(units.cm)) / RSun)
circ = patch.Circle((core_particle.x.value_in(units.cm) / RSun, core_particle.y.value_in(units.cm) / RSun), radius=core_particle.radius.value_in(units.m)[0] / RSun, fill=False, edgecolor="red")
ax.add_patch(circ)
plt.xlabel("x [RSun]")
plt.ylabel("y [RSun]")
plt.show()