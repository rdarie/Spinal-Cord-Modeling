# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 10:50:54 2016

@author: Radu
"""

from neuron import h
from clarke import ClarkeRelay
import numpy
from neuronpy.util import spiketrain

class ClarkeNetwork:
    """
    """
    def __init__(self, N=5):
        """
        :param N: Number of cells.
        """
        self._N = N              # Total number of cells in the net
        self.cells = []          # Cells in the net
        self.nclist = []         # NetCon list
        self.stim = None         # Stimulator
        self.gidlist = []        # List of global identifiers on this host
        
        self.t_vec = h.Vector()   # Spike time of all cells
        self.id_vec = h.Vector()  # Ids of spike times
        #### Make a new ParallelContext object
        self.pc = h.ParallelContext()

        
        self.set_numcells(N)  # Actually build the net.
    #
        
    def set_gids(self):
        """Set the gidlist on this host."""
        self.gidlist = []
        #### Round-robin counting.
        #### Each host as an id from 0 to pc.nhost() - 1.
        for i in range(int(self.pc.id()), self._N, int(self.pc.nhost())):
            self.gidlist.append(i)

    def set_numcells(self, N, radius=50):
        """Create, layout, and connect N cells."""
        self._N = N
        self.set_gids() #### Used when creating and connecting cells
        self.create_cells(N)
        self.connect_cells()
        self.connect_stim()
    #
    def create_cells(self, N):
        """Create and layout N cells in the network."""
        self.cells =    []
        self.cells_t1 = []
        self.cells_t2 = []
        self.cells_t3 = []
        self.cells_t4 = []
        self.cells_t5 = []
        r = 50 # Radius of cell locations from origin (0,0,0) in microns
        N = self._N
        for i in range(N):
            # Create and position cells
            clarke_1 = ClarkeRelay()
            clarke_1.set_position(0, 0, i*r)
            self.cells.append(clarke_1)
            self.cells_t1.append(clarke_1)
            
            clarke_2 = ClarkeRelay()
            clarke_2.set_position(0, r, i*r)
            self.cells.append(clarke_2)
            self.cells_t2.append(clarke_2)
            
            clarke_3 = ClarkeRelay()
            clarke_3.set_position(0, 2*r, i*r)
            self.cells.append(clarke_3)
            self.cells_t3.append(clarke_3)
            
            clarke_4 = ClarkeRelay()
            clarke_4.set_position(0, 3*r, i*r)
            self.cells.append(clarke_4)
            self.cells_t4.append(clarke_4)
            
            clarke_5 = ClarkeRelay()
            clarke_5.set_position(0, 4*r, i*r)
            self.cells.append(clarke_5) 
            self.cells_t5.append(clarke_5) 
    #
    def connect_cells(self):
        """Connect cell n to cell n + 1."""
        self.nclist = []
    #
    def connect_stim(self):
        """Connect a spiking generator to the first cell to get
        the network going."""
        #create stimulators
        N = self._N
        self.iaf_list = []
        self.iae_list = []
        self.iie_list = []
        self.ibe_list = []
        self.fra_list = []
        
        for i in range(N):
            iaf = h.NetStim()
            iaf.interval = 100
            iaf.number = 1e9
            iaf.start = 0
            iaf.noise = 0.5
            self.iaf_list.append(iaf)
            
            iae = h.NetStim()
            iae.interval = 100
            iae.number = 1e9
            iae.start = 0
            iae.noise = 0.5
            self.iae_list.append(iae)
            
            iie = h.NetStim()
            iie.interval = 1000
            iie.number = 1e9
            iie.start = 0
            iie.noise = 0.5
            self.iie_list.append(iie)
            
            ibe = h.NetStim()
            ibe.interval = 50
            ibe.number = 1e9
            ibe.start = 0
            ibe.noise = 0.5
            self.ibe_list.append(ibe)
            
            fra = h.NetStim()
            fra.interval = 75
            fra.number = 1e9
            fra.start = 0
            fra.noise = 0.5
            self.fra_list.append(fra)
        
        
        numpy.random.seed(123)
        p = 50e-2
        syn_weight = 5e-3
        for i in range(N): 
            Y_iaf_t1 = numpy.random.binomial(1, p, N) # 5% probability of an inh.
                                                    #connection to Ia_flex
            Y_iae_t1 = numpy.random.binomial(1, p, N) # 5% probability of an ex.
                                                    #connection to Ia_extensor
            Y_ibe_t1 = numpy.random.binomial(1, p, N) # 5% probability of an inh.
                                                    #connection to Ib_extensor
            
            Y_iae_t2 = numpy.random.binomial(1, p, N) # 5% probability of an ex.
                                                    #connection to Ia_extensor
            Y_iie_t2 = numpy.random.binomial(1, p, N) # 5% probability of an ex.
                                                    #connection to II_extensor
            Y_ibe_t2 = numpy.random.binomial(1, p, N) # 5% probability of an inh.
                                                    #connection to Ib_extensor
            
            Y_iae_t3 = numpy.random.binomial(1, p, N) # 5% probability of an ex.
                                                    #connection to Ia_extensor
            Y_ibe_t3 = numpy.random.binomial(1, p, N) # 5% probability of an ex.
                                                    #connection to Ib_extensor
            Y_fra_t3 = numpy.random.binomial(1, p, N) # 5% probability of an inh.
                                                    #connection to FRA
            
            Y_ibe_t4 = numpy.random.binomial(1, p, N) # 5% probability of an ex.
                                                    #connection to Ib_extensor
                        
            Y_ibe_t5 = numpy.random.binomial(1, p, N) # 5% probability of an ex.
                                                    #connection to Ib_extensor
            Y_iie_t5 = numpy.random.binomial(1, p, N) # 5% probability of an ex.
                                                    #connection to II_extensor
            Y_fra_t5 = numpy.random.binomial(1, p, N) # 5% probability of an inh.
                                                    #connection to FRA
            
            for k in range(N):
                if Y_iaf_t1[k]:
                    ncstim = h.NetCon(self.iaf_list[k], self.cells_t1[i].synlist[1]) #inh
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                if Y_iae_t1[k]:
                    ncstim = h.NetCon(self.iae_list[k], self.cells_t1[i].synlist[0]) #ex
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                if Y_ibe_t1[k]:
                    ncstim = h.NetCon(self.ibe_list[k], self.cells_t1[i].synlist[1]) #inh
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                
                if Y_iae_t2[k]:
                    ncstim = h.NetCon(self.iae_list[k], self.cells_t2[i].synlist[0]) #ex
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                if Y_iie_t2[k]:
                    ncstim = h.NetCon(self.iie_list[k], self.cells_t2[i].synlist[2]) #II ex
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                if Y_ibe_t2[k]:
                    ncstim = h.NetCon(self.ibe_list[k], self.cells_t1[i].synlist[1]) #inh
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                    
                if Y_iae_t3[k]:
                    ncstim = h.NetCon(self.iae_list[k], self.cells_t3[i].synlist[0]) #ex
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                if Y_ibe_t3[k]:
                    ncstim =  h.NetCon(self.ibe_list[k], self.cells_t3[i].synlist[0]) #ex
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                if Y_fra_t3[k]:
                    ncstim = h.NetCon(self.fra_list[k], self.cells_t3[i].synlist[1]) #inh
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                    
                if Y_ibe_t4[k]:
                    ncstim = h.NetCon(self.ibe_list[k], self.cells_t4[i].synlist[0]) #ex
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                    
                if Y_ibe_t5[k]:
                    ncstim = h.NetCon(self.ibe_list[k], self.cells_t5[i].synlist[0]) #ex
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                if Y_iie_t5[k]:
                    ncstim = h.NetCon(self.iie_list[k], self.cells_t5[i].synlist[0]) #ex
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                if Y_fra_t5[k]:
                    ncstim = h.NetCon(self.fra_list[k], self.cells_t5[i].synlist[1]) #inh
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
            
            
            for i in range(len(self.nclist)):
                self.nclist[i].record(self.t_vec, self.id_vec, i)

    #
    def get_spikes(self):
        """Get the spikes as a list of lists."""
        return spiketrain.netconvecs_to_listoflists(self.t_vec, self.id_vec)