import helper_functions as hf
from neuron import h
from Network_LFPy import Network
from Ia_LFPy import Ia
from Mn_LFPy import Mn

class Ia_network(Network):
    #
    def __init__(self, *args, **kwargs):
        '''
        class initialization

        POPULATION_SIZE :       int, number of cells
        cellParameters :        dict
        populationParameters :  dict
        synapseParameters :     dict

        '''
        super(Ia_network, self).__init__(*args, **kwargs)

        self.cellPositions = {
            'Mn' : [],
            'Ia' : []
        }
        
        self.cellRotations = {
            'Mn' : [],
            'Ia' : []
        }
    #

    def create_cells(self, cellindex):
        """Create and layout N cells in the network."""
        cells = {}

        position_factor = 5e3;
        sim_params = hf.get_net_params(hf.get_tempdata_address())
        mn_pos_x = sim_params[10]
        mn_pos_y = sim_params[11]
        mn_pos_z = sim_params[12]

        cell = Mn()
        cell.set_pos(mn_pos_x[0] + cellindex * position_factor,
                          mn_pos_y[0] + cellindex * position_factor,
                          mn_pos_z[0] + cellindex * position_factor)
        cells.update({"Mn" : cell})
        self.cellPositions['Mn'].append([cell.somapos[0], cell.somapos[1], cell.somapos[2]])

        cell = Ia(n_nodes = 43)
        cell.set_pos(cellindex * position_factor,
                          cellindex * position_factor,
                          cellindex * position_factor)
        cells.update({"Ia" : cell})
        self.cellPositions['Ia'].append([cell.somapos[0], cell.somapos[1], cell.somapos[2]])

        return cells
    #
    def connect_cells(self, cells, cellindex):
            src = cells["Ia"]
            tgt_syn = cells["Mn"].synlist[0]
            nc = src.connect2target(src.Ia_node[0], tgt_syn)
            nc.weight[0] = self._synapseParameters['weight'][0]
            nc.delay = self._synapseParameters['weight'][0]

            return nc
    #
    def cellsim(self, cellindex):
        cells = self.create_cells(cellindex)
        nc = self.connect_cells(cells, cellindex)

        spiketimes = h.Vector()     # Spike time of all cells
        cell_ids = h.Vector()       # Ids of spike times
        nc.record(spiketimes, cell_ids, cellindex)

        #perform NEURON simulation, results saved as attributes in cell
        self.simulate(cells)

        shape_window = h.PlotShape()
        input('Pick a card, any card')

        print("nsoma_sec = %d" % cells['Mn'].nsomasec)
        #return dict with primary results from simulation
        return {'somav' : cells['Mn'].somav}

    def simulate(self,cells):
        """Run the simulation"""
        cells['Mn'].simulate(rec_vmem=True)
        cells['Ia'].simulate(rec_vmem=True)
