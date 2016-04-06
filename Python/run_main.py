from neuron import h
h.load_file('noload.hoc')
from mpi4py import MPI
from matplotlib import pyplot
from neuronpy.graphics import spikeplot
import get_net_params as np

h('systype = unix_mac_pc()')

if h.systype == 3:
    tempdata_address = "..\\..\\tempdata\\"
    mn_geom_address = "mn_geometries\\"
    slash = "\\"
else:
    tempdata_address = "../tempdata/"
    mn_geom_address = "mn_geometries/"
    slash = "/"

Ia_geom_file = tempdata_address + "Ia_geometry"
mn_geom_file = mn_geom_address + "motoneuron_geometry"
mod_geom_file = tempdata_address + "model_tree.neu"

pc = h.ParallelContext()

sim_params = np.get_net_params(tempdata_address)

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

h.execute('{xopen(\"..\\net_params\")}')

h.execute('{xopen(\"..\\netbuild\")}')

#/////////////////////////////////////////////////////////////
# Debugging: override stim params manually set amplitude
fudge_factor = 5e4
h.execute('{xopen(\"..\\debug_statements\")}')
#/////////////////////////////////////////////////////////////
h.execute('{xopen(\"..\\vextandinit\")}')

