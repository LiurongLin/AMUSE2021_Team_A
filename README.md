# AMUSE2021_Team_A

<h2> Plan </h2>
- Evolve star to Red Giant (figure out how long we should evolve it) <br>
- Make a hydroblob (figure out how to do that with particles smaller than 1MEarth) <br>
- Add the Earth to the system <br>
- (Add Moon if it works) <br>

<h2> How to use the code? </h2>
<h3> mesa_gravity_hydro.py </h3>
This is the code to run the evolution. First it evolves the Sun, then it divides the Sun into a core and gas particle which can be added to the hydro code. After that the gravity particle (Earth) is added. <br>
<br>
To quickly check if the code runs: change the evolving_age, n and t_end to a smaller number (e.g. evolving_age=1e3 Myr, n=1, t_end=1).<br>
<br>
It creates the following files: <br>
- temperature_luminosity_sun_t_evolve={}Myr_z={}_eta={}.csv which contains the temperature [K], luminosity [Lsun], mass [Msun], radius [Rsun] and evolving age [Myr] of the Sun at every timestep in the stellar evolution. <br>
- gravity_particles_t_end={}yr_n={}_i={}_z={}.amuse which contains the gravity particle set (i.e. the Earth). <br>
- hydro_particles_t_end={}yr_n={}_i={}_z={}.amuse which contains the core and gas particles set of the Sun. <br>
- coordinates_t_end={}yr_n={}_z={}.csv which contains the x and y coordinates [cm] of the core, last index gas particle and Earth at every timestep in the gravity-hydro evolution. <br>
- ae_t_end={}yr_n={}_z={}.csv contains the semi-major axis [m] and eccentricity of the Earth at every timestep. <br>
- masses_core_gas_t_end={}yr_n={}_z={}.csv contains the masses [Msun] of the core and sum of the gas particles at every timestep. <br>
- time_for_loop_t_end={}yr_n={}_z={}.csv contains the evolving time [yr] at every timestep. <br>

<h3> HR_diagram.py </h3>


<h3> visualisation.py </h3>
