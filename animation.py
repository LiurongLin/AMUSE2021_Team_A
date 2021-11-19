import os
import imageio
from natsort import natsorted

# This code will make a movie of all files in the folder animation. 
# You would first have to pip install imageio, natsort and imageio-ffmpeg

t_end = 50
n = 5

# fps = frame per second
w = imageio.get_writer('coordinates_system_t_end={}yr_n={}.mp4'.format(t_end, n), format='FFMPEG', mode='I', fps=1)
images = os.listdir("animation")
images = natsorted(images, key=lambda y: y.lower())

for image in images:
	w.append_data(imageio.imread('animation/{}'.format(image)))
w.close()
