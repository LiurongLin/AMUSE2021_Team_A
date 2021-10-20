from amuse.lab import *
from amuse.units import (units, constants)
from amuse.couple import bridge
import matplotlib.pyplot as plt
import matplotlib.patches as patch
import numpy as np
from tqdm import tqdm
import sys

RSun = 696340e5

core = read_set_from_file("core_particle.amuse", "amuse", append_to_file=False)
gas = read_set_from_file("gas_particles.amuse", "amuse", append_to_file=False)[-100:]

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

# system.add_particle(core)
# system[2].name = "core"

print(system)

converter_gravity = nbody_system.nbody_to_si(system.mass.sum(), earth.position.length())
gravity = Huayno(converter_gravity)
gravity.particles.add_particles(system)

# channel = {"from system": system.new_channel_to(gravity),
        #    "to_system": gravity.particles.new_channel_to(system)}

converter_hydro = nbody_system.nbody_to_si(gas.mass.sum(), gas[-1].position.length())
hydro = Fi(converter_hydro)
hydro.dm_particles.add_particle(core)
hydro.gas_particles.add_particles(gas)
hydro.parameters.timestep = 1e-2 | units.yr

gravity_hydro = bridge.Bridge(use_threading=False)
gravity_hydro.add_system(gravity, (hydro,))
gravity_hydro.add_system(hydro, (gravity,))
gravity_hydro.timestep = 1e-2 | units.yr

model_time = 0 | units.yr
t_end = 1 | units.yr

while model_time < t_end:
    model_time += gravity_hydro.timestep
    print(model_time)
    gravity_hydro.evolve_model(model_time)

    # channel["from system"].copy()
    # channel["to_system"].copy()

gravity.stop()
hydro.stop()

# fig, ax = plt.subplots(figsize=(6, 6))
# plt.scatter(np.array(gas.x.value_in(units.cm)) / RSun, np.array(gas.y.value_in(units.cm)) / RSun)
# circ = patch.Circle((core.x.value_in(units.cm) / RSun, core.y.value_in(units.cm) / RSun), radius=core.radius.value_in(units.m)[0] / RSun, fill=False, edgecolor="red")
# ax.add_patch(circ)
# plt.scatter(earth.x.value_in(units.km), earth.y.value_in(units.km))
# plt.scatter(moon.x.value_in(units.km), moon.y.value_in(units.km))
# plt.xlabel("x [RSun]")
# plt.ylabel("y [RSun]")
# plt.show()