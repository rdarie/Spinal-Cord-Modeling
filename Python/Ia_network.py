from neuron import h
h.nrn_load_dll("E:\\Google Drive\\Github\\Spinal-Cord-Modeling\\nrnmech.dll")
import helper_functions as hf
from Ia_template import Ia
from Mn_template import Mn

class Ia_network:

    def __init__(self, N = 2, syn_w = 0.15, syn_delay = 1):
        self._N = N;
        self.cells = []             # Cells in the net
        self.nclist = []            # NetCon list
        self.syn_w = syn_w          # Synaptic weight
        self.syn_delay = syn_delay  # Synaptic delay
        self.t_vec = h.Vector()     # Spike time of all cells
        self.id_vec = h.Vector()    # Ids of spike times
        self.set_numcells(N)        # Actually build the net.
    #
    def set_numcells(self, N):
        """Create, layout, and connect N cells."""
        self._N = N
        self.create_cells(N)
        self.connect_cells()
        #self.connect_stim()
   #
    def create_cells(self, N):
        """Create and layout N cells in the network."""
        self.cells = []
        r = 50 # Radius of cell locations from origin (0,0,0) in microns
        N = self._N
        position_factor = 5e3;
        sim_params = hf.get_net_params(hf.get_tempdata_address())
        mn_pos_x = sim_params[10]
        mn_pos_y = sim_params[11]
        mn_pos_z = sim_params[12]

        for i in range(N):
            cell = Mn()
            cell.set_position(mn_pos_x[0]+i * position_factor,mn_pos_y[0]+i * position_factor,mn_pos_z[0]+i * position_factor)
            self.cells.append(cell)

        for i in range(N):
            cell = Ia()
            cell.set_position(i * position_factor,i * position_factor,i * position_factor)
            self.cells.append(cell)
    #
    def connect_cells(self):
        """Connect cell i to cell i + N."""
        self.nclist = []
        N = self._N
        for i in range(N):
            src = self.cells[N+i]
            tgt_syn = self.cells[i].synlist[0]
            nc = src.connect2target(src.Ia_node[0], tgt_syn)
            nc.weight[0] = self.syn_w
            nc.delay = self.syn_delay
            nc.record(self.t_vec, self.id_vec, i)
            self.nclist.append(nc)
    #
    '''def connect_stim(self):
        """Connect a spiking generator to the first cell to get
        the network going."""
        self.stim = h.NetStim()
        self.stim.number = self.stim_number
        self.stim.start = 9
        self.ncstim = h.NetCon(self.stim, self.cells[0].synlist[0])
        self.ncstim.delay = 1
        self.ncstim.weight[0] = self.stim_w # NetCon weight is a vector.'''
    #
    def get_spikes(self):
        """Get the spikes as a list of lists."""
        return spiketrain.netconvecs_to_listoflists(self.t_vec, self.id_vec)
