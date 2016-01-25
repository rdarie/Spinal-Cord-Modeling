# -*- coding: utf-8 -*-
"""
Created on Thu Jan 07 11:08:01 2016

@author: Radu
"""

from neuron import h
from matplotlib import pyplot

def set_recording_vectors(cell):
    """Set soma, dendrite, and time recording vectors on the cell.

    :param cell: Cell to record from.
    :return: the soma, dendrite, and time vectors as a tuple.
    """
    soma_v_vec = h.Vector()      # Membrane potential vector at soma
    dend_v_vec = h.Vector()      # Membrane potential vector at dendrite
    t_vec = h.Vector()           # Time stamp vector
    
    soma_m_vec = h.Vector()      # Sodium m parameter vector at soma
    soma_h_vec = h.Vector()      # Sodium m parameter vector at soma
    soma_n_vec = h.Vector()      # Potassium n parameter vector at soma
    soma_ina_vec = h.Vector()      # Potassium n parameter vector at soma
    soma_ikrect_vec = h.Vector()      # Potassium n parameter vector at soma
    soma_ical_vec = h.Vector()   # Potassium n parameter vector at soma
    soma_inap_vec = h.Vector()   # Potassium n parameter vector at soma
    soma_idap_vec = h.Vector()   # Potassium n parameter vector at soma
    soma_ican_vec = h.Vector()   # Potassium n parameter vector at soma
    soma_ikca_vec = h.Vector()   # Potassium n parameter vector at soma
    
    soma_v_vec.record(cell.soma(0.5)._ref_v)
    
    soma_m_vec.record(cell.soma(0.5)._ref_m_clarke)
    soma_h_vec.record(cell.soma(0.5)._ref_h_clarke)
    soma_inap_vec.record(cell.soma(0.5)._ref_inap_clarke)
    soma_ina_vec.record(cell.soma(0.5)._ref_ina_clarke)
    soma_ikrect_vec.record(cell.soma(0.5)._ref_ikrect_clarke)
    soma_idap_vec.record(cell.dap_syn_._ref_i)
    soma_n_vec.record(cell.soma(0.5)._ref_n_clarke)
    
    soma_ical_vec.record(cell.soma(0.5)._ref_icaL_clarke)
    soma_ican_vec.record(cell.soma(0.5)._ref_icaN_clarke)
    soma_ikca_vec.record(cell.soma(0.5)._ref_ikca_clarke)
    
    dend_v_vec.record(cell.dend(0.5)._ref_v)
    t_vec.record(h._ref_t)

    return soma_v_vec, soma_m_vec, soma_h_vec, soma_n_vec,\
     soma_inap_vec, soma_idap_vec, soma_ical_vec,\
     soma_ican_vec, soma_ikca_vec, soma_ina_vec, soma_ikrect_vec,\
     dend_v_vec, t_vec

def simulate(tstop=10000):
    """Initialize and run a simulation.

    :param tstop: Duration of the simulation.
    """
    h.tstop = tstop
    h.run()

def show_output(soma_v_vec, dend_v_vec, t_vec, new_fig=True):
    """Draw the output.

    :param soma_v_vec: Membrane potential vector at the soma.
    :param dend_v_vec: Membrane potential vector at the dendrite.
    :param t_vec: Timestamp vector.
    :param new_fig: Flag to create a new figure (and not draw on top
            of previous results)
    """
    if new_fig:
        pyplot.figure(figsize=(8,4)) # Default figsize is (8,6)
    soma_plot = pyplot.plot(t_vec, soma_v_vec, color='black')
    dend_plot = pyplot.plot(t_vec, dend_v_vec, color='red')
    pyplot.legend(soma_plot + dend_plot, ['soma', 'dend(0.5)'])
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')