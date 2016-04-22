debugging = 1

import os
from neuron import h
if debugging:
    from neuron import gui
else:
    h.load_file('noload.hoc')

from mpi4py import MPI
from matplotlib import pyplot
from neuronpy.graphics import spikeplot
import helper_functions as hf
import Ia_network as Ia_net

os.chdir('E:\\Google Drive\\Github\\Spinal-Cord-Modeling\\Python')

tempdata_address = hf.get_tempdata_address()
mn_geom_address = hf.get_mn_geom_address()
Ia_geom_file = tempdata_address + "Ia_geometry"
mn_geom_file = mn_geom_address + "motoneuron_geometry"
mod_geom_file = tempdata_address + "model_tree.neu"

pc = h.ParallelContext()

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
test_net = Ia_net.Ia_network(2,0.15,3)

#h.topology()
shape_window = h.PlotShape()

#/////////////////////////////////////////////////////////////
# Debugging: override stim params manually set amplitude
'''fudge_factor = 5e4
h('{xopen(\"debug_statements\")}')
#/////////////////////////////////////////////////////////////
h('{xopen(\"vextandinit\")}')
h.run()'''

#/////////////////////////////////////////////////////////////
input("Please press a key.")
