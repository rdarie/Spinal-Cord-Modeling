debugging = 1

import os, pdb
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
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
from Ib_network_LFPy import Ib_network as Ib_net
import numpy as np
import cPickle as pickle
import scipy

os.chdir('E:\\Google Drive\\Github\\Spinal-Cord-Modeling\\Python')

tempdata_address = hf.get_tempdata_address()
mn_geom_address = hf.get_mn_geom_address()
Ib_geom_file = tempdata_address + "Ib_geometry"
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
        'tstopms' : 2000,            #stop time of simulation
        'custom_code'  : [], #active decl.
}

#Synaptic parameters, corresponding to a NetCon synapse built into NEURON
synapseParameters = {
    'idx' : 0,               # insert synapse on index "0", the soma
    'e' : 0.,                # reversal potential of synapse
    'syntype' : 'Exp2Syn',   # conductance based double-exponential synapse
    'tau1' : 1.0,            # Time constant, rise
    'tau2' : 1.0,            # Time constant, decay
    'weight' : (0.5, 0),   # Synaptic weight
    'delay' : (1, 0),   # Synaptic delay
    'record_current' : False,# disable synapse current recording
}

#the number of cells in the population
POPULATION_SIZE = 1

#will draw random cell locations within cylinder constraints:
populationParameters = {
    'radius' : 20,
    'zmin' : -200,
    'zmax' : 200,
}

net = Ib_net(POPULATION_SIZE,
                     cellParameters,
                     populationParameters,
                     synapseParameters)
#
ev_list = hf.get_v_from_mat('E:\\Google Drive\\Github\\tempdata\\move_root_um_move_root_points_cs.mat',1)
#pdb.set_trace()
#ev_list = np.linspace(0,ev_list[0],20).tolist() + ev_list
#ev_list = ev_list + np.linspace(ev_list[-1],0,20).tolist()
fudge_factor = -2e5
ev = {"Ib" : fudge_factor * np.array(ev_list)}

#/////////////////////////////////////////////////////////////
# Debugging: override stim params manually set amplitude
#pdb.set_trace()
net.insert_voltage(ev, hf.square_wave)

net.run()
res = net.results
pickle.dump(res, open( "E:\\Google Drive\\Github\\tempdata\\Ib_net.p", "wb" ) )

#/////////////////////////////////////////////////////////////
input("Please press a key.")
