import helper_functions as hf

from neuron import h
#h.nrn_load_dll("E:\\Google Drive\\Github\\Spinal-Cord-Modeling\\Python\\nrnmech.dll")

import numpy as np

from Network_LFPy import Network
from Ia_LFPy import Ia
from Clarke_LFPy import Clarke
import pdb

class Ia_Clarke(Network):
    #
    def __init__(self, *args, **kwargs):
        '''
        class initialization

        POPULATION_SIZE :       int, number of cells
        cellParameters :        dict
        populationParameters :  dict
        synapseParameters :     dict

        '''
        super(Ia_Clarke, self).__init__(*args, **kwargs)

        self.cellPositions = {
            'Clarke' : [],
            'Ia' : []
        }

        self.cellRotations = {
            'Clarke' : [],
            'Ia' : []
        }

        sim_params = hf.get_net_params(hf.get_tempdata_address())
        dummy_Ia = Ia(n_nodes = hf.get_n_nodes_from_mat('E:\\Google Drive\\Github\\tempdata\\move_root_um_move_root_points_cs.mat',0))
        dummy_Clarke = Clarke()

        self.cellMorphologies = {
            'Clarke' : dummy_Clarke.morphology_address,
            'Ia' : dummy_Ia.morphology_address
        }

        del dummy_Ia, dummy_Clarke
    #

    def create_cells(self, cellindex):
        """Create and layout N cells in the network."""
        cells = {}

        position_factor = 1e3
        sim_params = hf.get_net_params(hf.get_tempdata_address())
        mn_pos_x = sim_params[10]
        mn_pos_y = sim_params[11]
        mn_pos_z = sim_params[12]

        cell = Clarke()
        '''cell.set_pos(mn_pos_x[0] + cellindex * position_factor,
                      mn_pos_y[0] + cellindex * position_factor,
                          mn_pos_z[0] + cellindex * position_factor)
'''
        cell.set_pos(cellindex * position_factor,
                          cellindex * position_factor,
                          cellindex * position_factor)
        cells.update({"Clarke" : cell})
        self.cellPositions['Clarke'].append([cell.somapos[0], cell.somapos[1], cell.somapos[2]])

        cell = Ia(n_nodes = hf.get_n_nodes_from_mat('E:\\Google Drive\\Github\\tempdata\\move_root_um_move_root_points_cs.mat',0))
        cell.set_pos(cellindex * position_factor,
                          cellindex * position_factor,
                          cellindex * position_factor)
        cells.update({"Ia" : cell})
        self.cellPositions['Ia'].append([cell.somapos[0], cell.somapos[1], cell.somapos[2]])

        for key, value in cells.iteritems():
            value.tstopms = self.cellParameters['tstopms']

        return cells
    #
    def connect_cells(self, cells, cellindex):
            src = cells["Ia"]
            tgt_syn = cells["Clarke"].synlist[0]
            nc = src.connect2target(src.Ia_node[0], tgt_syn)
            nc.weight[0] = self._synapseParameters['weight'][0]
            nc.delay = self._synapseParameters['delay'][0]

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
        #pdb.set_trace()
        somav = cells['Clarke'].somav
        iav = cells['Ia'].vmem
        tvec = cells['Ia'].tvec

        for key, value in cells.iteritems():
            del value
        del cells

        #print("nsoma_sec = %d" % cells['Mn'].nsomasec)
        #return dict with primary results from simulation
        return {'somav' : somav, 'iav' : iav, 'tvec' : tvec}

    def simulate(self,cells):
        """Run the simulation"""
        super(Ia_Clarke, self).simulate(cells)
        cells['Ia'].simulate(rec_vmem=True, rec_imem = True)
        cells['Clarke'].simulate(rec_vmem=True, rec_imem = True)
