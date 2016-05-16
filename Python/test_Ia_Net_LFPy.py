# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 14:12:00 2016

@author: Radu
"""

from neuron import h
from Ia_network_LFPy import Ia_network
#define cell parameters used as input to cell-class
h.nrn_load_dll("E:\\Google Drive\\Github\\Spinal-Cord-Modeling\\nrnmech.dll")
cellParameters = {
        'rm' : 30000,               # membrane resistance
        'cm' : 1.0,                 # membrane capacitance
        'Ra' : 150,                 # axial resistance
        'v_init' : -65,             # initial crossmembrane potential
        'e_pas' : -65,              # reversal potential passive mechs
        'passive' : True,           # switch on passive mechs
        'nsegs_method' : 'lambda_f',# method for setting number of segments,
        'lambda_f' : 10,            # segments are isopotential at frequency
        'timeres_NEURON' : 2**-3,   # dt of LFP and NEURON simulation.
        'timeres_python' : 2**-3,
        'tstartms' : -1,          #start time, recorders start at t=0
        'tstopms' : 2,            #stop time of simulation
        'custom_code'  : [], #active decl.
}

#Synaptic parameters, corresponding to a NetCon synapse built into NEURON
synapseParameters = {
    'idx' : 0,               # insert synapse on index "0", the soma
    'e' : 0.,                # reversal potential of synapse
    'syntype' : 'Exp2Syn',   # conductance based double-exponential synapse
    'tau1' : 1.0,            # Time constant, rise
    'tau2' : 1.0,            # Time constant, decay
    'weight' : (0.002, 0),   # Synaptic weight
    'record_current' : False,# disable synapse current recording
}

#the number of cells in the population
POPULATION_SIZE = 5

#will draw random cell locations within cylinder constraints:
populationParameters = {
    'radius' : 20,
    'zmin' : -200,
    'zmax' : 200,
}

bla = Ia_network(POPULATION_SIZE,
                     cellParameters,
                     populationParameters,
                     synapseParameters)
bla.run()
bla.plot_network()
#input('Pick a card, any card')