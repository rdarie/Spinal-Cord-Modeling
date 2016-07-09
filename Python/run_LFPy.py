debugging = 1

import os, pdb
from neuron import h
if debugging:
    from neuron import gui
else:
    h.load_file('noload.hoc')

import scipy
from scipy.interpolate import interp1d

from mpi4py import MPI
from matplotlib import pyplot
from neuronpy.graphics import spikeplot
import helper_functions as hf
from Ia_network_LFPy import Ia_network as Ia_net
import numpy as np
import cPickle as pickle

os.chdir('E:\\Google Drive\\Github\\Spinal-Cord-Modeling\\Python')

tempdata_address = hf.get_tempdata_address()
mn_geom_address = hf.get_mn_geom_address()
Ia_geom_file = tempdata_address + "Ia_geometry"
mn_geom_file = mn_geom_address + "motoneuron_geometry"
mod_geom_file = tempdata_address + "model_tree.neu"

sim_params = hf.get_net_params(tempdata_address)

# sim_params[0] = n_nodes
# sim_params[1] = start_time
# sim_params[2] = dur_time
# sim_params[3] = interval_time
# sim_params[4] = diameter
# sim_params[5] = inl
# sim_params[6] = points_per_node
# sim_params[7] = ampstart
# sim_params[8] = stepsize
# sim_params[9] = ampmax
# sim_params[10]= coords_x
# sim_params[11]= coords_y
# sim_params[12]= coords_z

#/////////////////////////////////////////////////////////////
# Instantiate Network:

debugging = 0

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
        'tstartms' : -1,            #start time, recorders start at t=0
        'tstopms' : 5000,            #stop time of simulation
        'custom_code'  : [], #active decl.
}

#Synaptic parameters, corresponding to a NetCon synapse built into NEURON
synapseParameters = {
    'idx' : 0,               # insert synapse on index "0", the soma
    'e' : 0.,                # reversal potential of synapse
    'syntype' : 'Exp2Syn',   # conductance based double-exponential synapse
    'tau1' : 1.0,            # Time constant, rise
    'tau2' : 1.0,            # Time constant, decay
    'weight' : (0.05, 0),   # Synaptic weight
    'record_current' : False,# disable synapse current recording
}

#the number of cells in the population
POPULATION_SIZE = 2

#will draw random cell locations within cylinder constraints:
populationParameters = {
    'radius' : 20,
    'zmin' : -200,
    'zmax' : 200,
}

net = Ia_net(POPULATION_SIZE,
                     cellParameters,
                     populationParameters,
                     synapseParameters)

ev_list = hf.get_comsol_voltage(tempdata_address)
ev = {"Ia" : np.array(ev_list)}
#/////////////////////////////////////////////////////////////
# Debugging: override stim params manually set amplitude
fudge_factor = 5e4
net.insert_voltage(ev, np.sin) # TODO wrong

net.run()
res = net.results
pickle.dump(res, open( "E:\\Google Drive\\Github\\tempdata\\test_net.p", "wb" ) )

#/////////////////////////////////////////////////////////////
input("Please press a key.")
