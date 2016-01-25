# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 19:19:32 2016

@author: Radu
"""

from neuron import h
h.load_file('stdgui.hoc')
from matplotlib import pyplot
from neuronpy.graphics import spikeplot

from Network import ClarkeNetwork
import simrun

def tweak_leak(cells, Ncells):
    for a in range(Ncells):
        cells[a].soma.el_clarke =\
        (cells[a].soma.ina_clarke + cells[a].soma.ikrect_clarke\
        + cells[a].soma.icaN_clarke + cells[a].soma.icaL_clarke\
        + cells[a].soma.ikca_clarke + cells[a].soma.inap_clarke\
        + cells[a].soma.gl_clarke*cells[a].soma.v) / cells[a].soma.gl_clarke
        
        cells[a].dend.e_pas =\
        (cells[a].dend.g_pas * cells[a].dend.v) / cells[a].dend.g_pas
#    print 'hello from inside init'

    
h.celsius = 37
net = ClarkeNetwork()
h.v_init = -65
fih = h.FInitializeHandler(2,(tweak_leak,(net.cells,len(net.cells))))
shape_window = h.PlotShape()
shape_window.exec_menu('Show Diam')
soma_v_vec, soma_m_vec, soma_h_vec, soma_n_vec,\
     soma_inap_vec, soma_idap_vec, soma_ical_vec,\
     soma_ican_vec, soma_ikca_vec, soma_ina_vec, soma_ikrect_vec,\
    dend_v_vec, t_vec\
    = simrun.set_recording_vectors(net.cells[0])
   

simrun.simulate(tstop=10000)
simrun.show_output(soma_v_vec, dend_v_vec, t_vec)
pyplot.show()
spikes = net.get_spikes()
sp = spikeplot.SpikePlot(savefig=True)
sp.plot_spikes(spikes)