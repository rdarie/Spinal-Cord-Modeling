# -*- coding: utf-8 -*-
"""
Created on Thu Jan 07 11:08:41 2016

@author: Radu
"""

import numpy
import simrun
from ballandstick_clarke import BallAndStick
from neuron import h, gui
from math import sin, cos, pi
from matplotlib import pyplot
from itertools import izip
from neuronpy.graphics import spikeplot
from neuronpy.util import spiketrain

def tweak_leak(cells, Ncells):
    #h.t = -1e10
    #dtsav = h.dt
    #h.dt = 1e9
    #if cvode is on, turn it off to do large fixed step
    #temp = h.cvode.active()
    #if temp!=0:
    #    h.cvode.active(0)
    #while t<-1e9:
    #    h.fadvance()
    # restore cvode if necessary
    #if temp!=0:
    #    h.cvode.active(1)
    #h.dt = dtsav

    #h.t = 0
    for a in range(Ncells):
        #cells[a].soma.e_pas =\
        #(cells[a].soma.ina + cells[a].soma.ik\
        #+ cells[a].soma.icaN_motoneuron + cells[a].soma.icaL_motoneuron\
        #+ cells[a].soma.ikca_motoneuron + cells[a].soma.il_motoneuron\
        #+ cells[a].soma.ikrect_motoneuron\
        #+ cells[a].soma.g_pas*cells[a].soma.v) / cells[a].soma.g_pas
        #
        #cells[a].dend.e_pas =\
        #(cells[a].dend.g_pas * cells[a].dend.v) / cells[a].dend.g_pas
        cells[a].soma.el_motoneuron =\
        (cells[a].soma.ina_motoneuron + cells[a].soma.ikrect_motoneuron\
        + cells[a].soma.icaN_motoneuron + cells[a].soma.icaL_motoneuron\
        + cells[a].soma.ikca_motoneuron\
        + cells[a].soma.gl_motoneuron*cells[a].soma.v) / cells[a].soma.gl_motoneuron
        
        cells[a].dend.e_pas =\
        (cells[a].dend.g_pas * cells[a].dend.v) / cells[a].dend.g_pas
    print 'hello from inside init'
    #h('t = -1e6')
    #h('dtsav = dt')
    #h('dt = 1')
    #h('temp = cvode.active()')
    #h('if (temp!=0) { cvode.active(0) }')
    #h('while (t<-0.5e6) { fadvance() }')
    #h('if (temp!=0) { cvode.active(1) }')
    #h('dt = dtsav')
    #h('t = 0')
    
cells = []
N = 5
r = 50 # Radius of cell locations from origin (0,0,0) in microns
for i in range(N):
    cell = BallAndStick()
    # When cells are created, the soma location is at (0,0,0) and
    # the dendrite extends along the X-axis.
    # First, at the origin, rotate about Z.
    cell.rotateZ(i*2*pi/N)
    # Then reposition
    x_loc = sin(i * 2 * pi / N) * r
    y_loc = cos(i * 2 * pi / N) * r
    cell.set_position(x_loc, y_loc, 0)
    cells.append(cell)

h.celsius = 37

shape_window = h.PlotShape()
shape_window.exec_menu('Show Diam')

#stim = h.NetStim() # Make a new stimulator

# Attach it to a synapse in the middle of the dendrite
# of the first cell in the network. (Named 'syn_' to avoid
# being overwritten with the 'syn' var assigned later.)
#syn_ = h.ExpSyn(cells[0].dend(0.5))
#syn_.tau = 10
#stim.number = 1
#stim.start = 9

#ncstim = h.NetCon(stim, syn_)
#ncstim.delay = 1
#ncstim.weight[0] = 0.0075 # NetCon weight is a vector.

stim = h.IClamp(cells[0].soma(0.5))
stim.delay = 50
stim.dur = 2
stim.amp = 0.2

soma_v_vec, soma_m_vec, soma_h_vec, soma_n_vec,\
     soma_inap_vec, soma_idap_vec, soma_ical_vec,\
     soma_ican_vec, soma_ikca_vec, soma_ina_vec, soma_ikrect_vec,\
    dend_v_vec, t_vec\
    = simrun.set_recording_vectors(cells[0])

# Set recording vectors
syn_i_vec = h.Vector()
syn_i_vec.record(stim._ref_i)

h.v_init = -65
fih = h.FInitializeHandler(2,(tweak_leak,(cells,N)))

simrun.simulate()

# Draw
fig = pyplot.figure(figsize=(8,4))
ax1 = fig.add_subplot(2,1,1)
soma_plot = ax1.plot(t_vec, soma_v_vec, color='black')
dend_plot = ax1.plot(t_vec, dend_v_vec, color='red')
#rev_plot = ax1.plot([t_vec[0], t_vec[-1]], [syn_.e, syn_.e],
#        color='blue', linestyle=':')
ax1.legend(soma_plot + dend_plot,
        ['soma', 'dend(0.5)', 'syn reversal'])
ax1.set_ylabel('mV')
ax1.set_xlim([25,125])
#ax1.set_xticks([]) # Use ax2's tick labels

ax2 = fig.add_subplot(2,1,2, sharex = ax1)
syn_plot = ax2.plot(t_vec, syn_i_vec, color='blue')
ax2.legend(syn_plot,\
 ['injected current'])
ax2.set_ylabel(h.units('ExpSyn.i'))
ax2.set_xlabel('time (ms)')
ax2.set_xlim([25,125])
pyplot.show()

# Draw
fig2 = pyplot.figure(figsize=(8,4))

ax1 = fig2.add_subplot(3,1,1)
soma_plot = ax1.plot(t_vec, soma_v_vec, color='black')

ax1.legend(soma_plot,'soma')
ax1.set_ylabel('mV')
ax1.set_xlim([25,125])
ax1.set_ylim([-75,-65])

ax2 = fig2.add_subplot(3,1,2, sharex = ax1)
m_plot = ax2.plot(t_vec, soma_m_vec, color='blue')
h_plot = ax2.plot(t_vec, soma_h_vec, color='red')
n_plot = ax2.plot(t_vec, soma_n_vec, color='black')
ax2.legend(m_plot + h_plot + n_plot, ['m', 'h', 'n'])

ax2.set_xlabel('time (ms)')
ax2.set_xlim([25,125])

ax3 = fig2.add_subplot(3,1,3, sharex = ax1)
cal_plot = ax3.plot(t_vec, soma_ical_vec, color='blue')
can_plot = ax3.plot(t_vec, soma_ican_vec, color='red')
kca_plot = ax3.plot(t_vec, soma_ikca_vec, color='black')
ax3.legend(cal_plot + can_plot + kca_plot, ['CaL', 'CaN', 'KCa'])

ax3.set_xlabel('time (ms)')
ax3.set_xlim([25,125])

pyplot.show()