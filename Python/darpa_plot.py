debugging = 1

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
import os, pdb
from neuron import h
if debugging:
    from neuron import gui
else:
    h.load_file('noload.hoc')

import scipy
from scipy.interpolate import interp1d

from matplotlib import pyplot as plt
from neuronpy.graphics import spikeplot
from Ia_network_LFPy import Ia_network as Ia_net
import numpy as np
import cPickle as pickle
from helper_functions import *

filename = "E:\\Google Drive\\Github\\tempdata\\Iab_net.p"
location = -1
nameout = 'Iab-Mn-terminal'
data = pickle.load( open(filename, "rb" ) )
# decimate data for plotting
decimate_t = 1
decimate_s = 1
nproc = len(data)
ia_plot = []
ib_plot = []
iaint_plot = []
ibint_plot = []
mn_plot = []
ren_plot = []
t_plot = []

#
t_plot.append(data[0]['tvec'][::decimate_t])
for proc in range(len(data)):
    #pdb.set_trace()
    ia_plot.append(data[proc]['iav'][location, ::decimate_t])
    ib_plot.append(data[proc]['ibv'][location, ::decimate_t])
    iaint_plot.append(data[proc]['iav'][0, ::decimate_t])
    ibint_plot.append(data[proc]['ibv'][0, ::decimate_t])
    ren_plot.append(data[proc]['renv'][0, ::decimate_t])
    mn_plot.append(data[proc]['mnv'][::decimate_t])
#pdb.set_trace()
data_plot3d = []
dx = 1
dt = 1
for proc in range(len(data)):
    data_plot3d.append(data[proc]['ibv'][::decimate_s, ::decimate_t])

nseg, nsamp = data_plot3d[0].shape
x = np.arange(nseg)

t_plot = []
t_plot.append(data[0]['tvec'][::decimate_t])
y = t_plot[0]

X,Y = np.meshgrid(x, y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

mlab.figure(1, fgcolor=(0, 0, 0), bgcolor=(1, 1, 1))

s = mlab.surf(data_plot3d[0], warp_scale="auto", extent = [0,1,0,5,0,1])
#pdb.set_trace()
ax=mlab.axes(s, ranges = [0, 43.306, np.min(y), np.max(y), np.min(data_plot3d[0]), np.max(data_plot3d[0])])
#
ax.axes.label_format='%.2f'
ax.label_text_property.font_family = 'arial'
mlab.xlabel('Distance along axon (mm)')
mlab.ylabel('Time (msec)')
mlab.zlabel('Membrane voltage (mV)')

ax.axes.font_factor=0.9
mlab.savefig('3d_voltage.png', size=(1920, 1080))

fig = plt.figure()
ax = fig.add_subplot(211)

ia_plot, = ax.plot(t_plot[0], ia_plot[0], label = 'Axon terminal')
mn_plot, = ax.plot(t_plot[0], mn_plot[0], label = 'Motoneuron soma')
stim_plot, = ax.plot(t_plot[0], square_wave(t_plot[0]), label = 'Stimulus waveform')
plt.xlabel('Time (msec)')
plt.ylabel('Membrane Voltage (mV)')
lgd1 = ax.legend(handles=[ia_plot, mn_plot, stim_plot], loc='center left', bbox_to_anchor=(1, 0.5))
# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])

ax = fig.add_subplot(212)

iaint_plot, = ax.plot(t_plot[0], iaint_plot[0], label = 'Ia Interneuron')
ibint_plot, = ax.plot(t_plot[0], ibint_plot[0], label = 'Ib Interneuron')
ren_plot, = ax.plot(t_plot[0], ren_plot[0], label = 'Renshaw Cell')
plt.xlabel('Time (msec)')
plt.ylabel('Membrane Voltage (mV)')
lgd2 = ax.legend(handles=[iaint_plot, ibint_plot, ren_plot], loc='center left', bbox_to_anchor=(1, 0.5))
 Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])

plt.show()
fig.savefig(nameout + '.png', dpi=300, format='png', bbox_extra_artists=(lgd1,), bbox_inches='tight')
