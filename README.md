# AMUSE2021_Team_A

<h2> Plan </h2>
- Evolve star to Red Giant (what should be the evolving time?) <br>
- Make a hydroblob <br>
- Add the Earth to the system <br>
- (Add Moon if possible) <br>

<h2> Software required </h2>
This code uses the AMUSE software. For more information go to: https://www.amusecode.org/

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
Use this code to make an HR-diagram for the Sun (luminosity against temperature) during its stellar evolution.

<h3> sun_visualisation.py </h3>

Use this code to visualise the temperature, luminosity, mass, radius or evolving age of the Sun. 

<h3> visualisation.py </h3>
Use this code to make a plot of the coordinates of the core and gas particles together with the Earth coordinates. Where the Earth will be visualised with a color corresponding to the evolving time.

<h2> Results </h2>
The following folders contain the results of specific runs:<br>
- t_end={}_n={}_z={} contain the result of a normal run with the parameters given in the name of the folder. <br>
- t_end={}_n={}_z={}_e0 same as the above, except that there is an extra condition in the while loop of the stellar evolution. The conditions here are that it should evolve to at least 12 Gyr and in addition, the Sun's radius should correspond to 0.9 au. <br>
- r_roche={}_t_end={}_n={}_z={} same as the above folder but now with a Sun's radius corresponding to 0.5 au. <br>
- t_evolve={}_t_end={}_n={}_diff_v only evolved until 12 Gyr (without extra condition), but changed the velocity corresponding with the Earth's position after the stellar evolution. <br>
- eccentricity_vs_time contains plots of the eccentricity as a function of time for different values of t_end and n. <br>
<br>
More results can be found in the 'Liurong' branch. 

The final results that are presented in the report are in the "Liurong" branch.
The following folders contain the ".csv" file of the eccentricity along time and ".amuse" files of the final stage of the core and gas particles of the Sun.<br>
- t_end={}_n={}_{}, where the last {} represents the final stage of the stellar evolution code, which is: <br>
  - 12Gyr: initally evolve the Sun to the age of 12 Gyr <br>
  - 12Gyr_moon: initally evolve the Sun to the age of 12 Gyr <br>
  - 12.05Gyr: initally evolve the Sun to the age of 12.05 Gyr <br>
  - 0.9AU: initally evolve the Sun to have a radius of 0.9 AU <br>
  - 0.9AU_no_friction: initally evolve the Sun to have a radius of 0.9 AU and neglect the friction caused by the envelope of the Sun <br>

<h3> plot_eccentricity_vs_t.ipynb </h3>
Use this code to make the eccentricity against time plots.

<h3> coordinates_plot.ipynb </h3>
Use this code to make the trajectory of the earth after we add it into the solar system.

<h3> eccentricity_vs_time </h3>
Folder that saves the eccentricity against time plots.

<h3> new_v </h3>
Folder that saves the plots of the trajectory of the Earth.
