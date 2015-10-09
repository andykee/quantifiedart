from math import sqrt
from os import listdir
from os.path import isfile, join

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import gpxpy

data_path = 'data'
plotarea = 'losangeles'
distance_threshold = 0.03
#figwidth = 3.0
colormap = {'transport':'deepskyblue',
            'walking':'darkorange',
            'cycling':'chartreuse'}
plotbounds = {
    'sandiego' : {'xmin':-117.5, 'xmax':-116.3, 'ymin':32.65, 'ymax':33.3},
    'losangeles' : {'xmin':-119.4, 'xmax':-117, 'ymin':33.3, 'ymax':34.4},
    'montana'  : {'xmin':-112, 'xmax':-110.8, 'ymin':45.2, 'ymax':46.0},
    'dewey': {'xmin':-75.10, 'xmax':-75.07, 'ymin':38.69, 'ymax':38.73}}

def deline(lat, lon):
    if len(lat) == len(lon):
        length = len(lat)
        i = 1
        while i < length:
            lat2 = lat[i]
            lat1 = lat[i-1]
            lon2 = lon[i]
            lon1 = lon[i-1]
            d = sqrt((lon2-lon1)**2 + (lat2-lat1)**2)
            if d > distance_threshold:
                lat.insert(i,np.nan)
                lon.insert(i,np.nan)
                i += 2
            else:
                i += 1
        return lat, lon
    else:
        print("Cannot deline data, lists must be same length")
        return lat, lon

def plot_data(filename, linecolor):
    lat = []
    lon = []
    gpx_filename = join(data_path,filename)
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)
        lat, lon = deline(lat, lon)
        ax.plot(lon, lat, color = linecolor, lw = 0.1, alpha = 0.8)
        lat = []
        lon = []

fig = plt.figure(facecolor = '0.05')
try:
    fig.set_figwidth(figwidth)
except:
    pass
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_xlim([plotbounds[plotarea]['xmin'],plotbounds[plotarea]['xmax']])
ax.set_ylim([plotbounds[plotarea]['ymin'],plotbounds[plotarea]['ymax']])
ax.set_axis_off()
fig.add_axes(ax)

data = [f for f in listdir(data_path) if isfile(join(data_path,f))]

for activity in data:
    filename = join(data_path,activity)
    activity_name = activity[:-4]
    if activity_name in colormap:
        linecolor = colormap[activity_name]
    plot_data(filename, linecolor)

filename = plotarea + '.png'
plt.savefig(filename, facecolor = '0.05', bbox_inches='tight', pad_inches=0, dpi=1000)
