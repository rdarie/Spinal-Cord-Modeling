# -*- coding: utf-8 -*-
"""
Created on Thu Jan 07 11:08:41 2016

@author: Radu
"""

import numpy
import simrun
import time
from ballandstick_clarke import BallAndStick

#from neuron import h,gui
from neuron import h
h.load_file('stdgui.hoc')
#h.load_file("stdrun.hoc")
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
        #+ cells[a].soma.icaN_clarke + cells[a].soma.icaL_clarke\
        #+ cells[a].soma.ikca_clarke + cells[a].soma.il_clarke\
        #+ cells[a].soma.ikrect_clarke\
        #+ cells[a].soma.g_pas*cells[a].soma.v) / cells[a].soma.g_pas
        #
        #cells[a].dend.e_pas =\
        #(cells[a].dend.g_pas * cells[a].dend.v) / cells[a].dend.g_pas
        cells[a].soma.el_clarke =\
        (cells[a].soma.ina_clarke + cells[a].soma.ikrect_clarke\
        + cells[a].soma.icaN_clarke + cells[a].soma.icaL_clarke\
        + cells[a].soma.ikca_clarke + cells[a].soma.inap_clarke\
        + cells[a].soma.gl_clarke*cells[a].soma.v) / cells[a].soma.gl_clarke
        
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
N = 3
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
    
cellSurface = h.area(0.5, sec = cells[0].soma)
h.celsius = 37
#shape_window = h.PlotShape()
#shape_window.exec_menu('Show Diam')

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

#Stims and clamps
stim = h.IClamp(cells[0].soma(0.5))
stim.delay = 200
stim.dur = 2

#clamp = h.SEClamp(cells[0].soma(0.5))
#clamp.dur1 = 1e9
#clamp.amp1 = -65
#clamp.rs = 1e2

stim2 = h.IClamp(cells[0].soma(0.5))
stim2.delay = 500
stim2.dur = 300

stim2.amp = 0
stim.amp = 5e-1-stim2.amp
#stim.amp = 0

soma_v_vec, soma_m_vec, soma_h_vec, soma_n_vec,\
     soma_inap_vec, soma_idap_vec, soma_ical_vec,\
     soma_ican_vec, soma_ikca_vec, soma_ina_vec, soma_ikrect_vec,\
    dend_v_vec, t_vec\
    = simrun.set_recording_vectors(cells[0])

# Set recording vectors
syn_i_vec = h.Vector()
syn_i_vec.record(stim._ref_i)

#h('v_init = 89')
h.v_init = -65
fih = h.FInitializeHandler(2,(tweak_leak,(cells,N)))


# Draw
fig1 = pyplot.figure(figsize=(8,4))
ax1a = fig1.add_subplot(2,1,1)
ax2a = fig1.add_subplot(2,1,2, sharex = ax1a)

fig2 = pyplot.figure(figsize=(5,16))
ax1b = fig2.add_subplot(3,1,1)
ax2b = fig2.add_subplot(3,1,2, sharex = ax1b)
ax3b = fig2.add_subplot(3,1,3, sharex = ax1b)
ax1b.set_xlim([150,500])
ax1b.set_ylim([-72,-60])

#step = 2.5e-2 #CaN
#step = 1e-5 #CaL
#step = 5e-2 #KCa
#step = 4e-5 #napbar
#step = 5 #tau_mc
#step = 1 #tau_hc
#step = 1e-3 #dap weight
#step = 5e-2 # gkrect
#step = 0.01 #Na
#step = 5 #tau_mp_bar
#step = 1 # tau_n_bar
step = 1e-2 #stim2
num_steps = 1
h.dt = 0.01

for i in numpy.linspace(0, step*num_steps, num_steps):
    #stim2.amp += step 
    for a in range(N):
        pass
        #cells[a].soma.gcaN_clarke = cells[a].soma.gcaN_clarke + step
        #cells[a].soma.gcaL_clarke = cells[a].soma.gcaL_clarke + step
        #cells[a].soma.gcak_clarke = cells[a].soma.gcak_clarke + step
        #cells[a].soma.gnapbar_clarke = cells[a].soma.gnapbar_clarke + step
        #cells[a].soma.tau_mc_clarke = cells[a].soma.tau_mc_clarke + step
        #cells[a].soma.tau_hc_clarke = cells[a].soma.tau_hc_clarke + step
        #cells[a].dap_nc_.weight[0] = cells[a].dap_nc_.weight[0] +step  
        #cells[a].soma.gkrect_clarke = cells[a].soma.gkrect_clarke + step      
        #cells[a].soma.tau_mp_bar_clarke = cells[a].soma.tau_mp_bar_clarke + step
        #cells[a].soma.tau_n_bar_clarke = cells[a].soma.tau_n_bar_clarke + step
        #cells[a].soma.gnabar_clarke = cells[a].soma.gnabar_clarke + step
    
    simrun.simulate()
    
    time.sleep(1)
    lWid = 1
    soma_plot = ax1a.plot(t_vec, soma_v_vec, color='black', lw=lWid)
    dend_plot = ax1a.plot(t_vec, dend_v_vec, color='red', lw=lWid)

    syn_plot = ax2a.plot(t_vec, syn_i_vec, color='blue', lw=lWid)
    ax2a.legend(syn_plot,\
        ['injected current'])

    lWid = 3
    soma_plot = ax1b.plot(t_vec, soma_v_vec, color='black', lw=lWid)

    m_plot = ax2b.plot(t_vec, soma_m_vec, color='blue', lw=lWid)
    h_plot = ax2b.plot(t_vec, soma_h_vec, color='red', lw=lWid)
    n_plot = ax2b.plot(t_vec, soma_n_vec, color='black', lw=lWid)

    cal_plot = ax3b.plot(t_vec, soma_ical_vec, color='blue', lw=lWid)
    can_plot = ax3b.plot(t_vec, soma_ican_vec, color='red', lw=lWid)
    #ina_plot = ax3b.plot(t_vec, soma_ina_vec, color='magenta', lw=lWid)
    #ikrect_plot = ax3b.plot(t_vec, soma_ikrect_vec, color='cyan', lw=lWid)
    kca_plot = ax3b.plot(t_vec, soma_ikca_vec, color='black', lw=lWid)
    nap_plot = ax3b.plot(t_vec, soma_inap_vec, color='green', lw=lWid)
    soma_idap_mAcm2 = numpy.array(soma_idap_vec.to_python())
    soma_idap_mAcm2 = soma_idap_mAcm2/(100*cellSurface)
    dap_plot = ax3b.plot(numpy.array(t_vec.to_python()),\
    soma_idap_mAcm2, color='orange', lw=lWid)
    #dap_plot = ax3b.plot(t_vec, soma_idap_vec, color='orange')

ax1a.legend(soma_plot + dend_plot,
       ['soma', 'dend(0.5)', 'syn reversal'])
ax1a.set_ylabel('mV')
ax1a.set_xlim([100,300])

ax2a.set_ylabel(h.units('ExpSyn.i'))
ax2a.set_xlabel('time (ms)')
ax1a.set_xlim([100,300])

ax1b.set_ylabel('mV')
ax1b.legend(soma_plot,'soma')

ax2b.legend(m_plot + h_plot + n_plot, ['m', 'h', 'n'])
ax2b.set_xlabel('time (ms)')
ax1a.set_xlim([100,300])

ax3b.legend(cal_plot + can_plot +\
 kca_plot + nap_plot + dap_plot,\
 ['CaL', 'CaN', 'KCa', 'NaP', 'DAP'])
ax3b.set_xlabel('time (ms)')
ax1a.set_xlim([100,300])
pyplot.show()
#h.quit()