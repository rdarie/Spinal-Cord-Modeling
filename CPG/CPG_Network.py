# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 10:50:54 2016

@author: Radu
"""

from neuron import h
from ib_in import Ib_in
from ia_in import Ia_in
from rc_in import Renshaw
from motoneuron import Motoneuron

import numpy
from neuronpy.util import spiketrain

class ReflexNetwork:
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
        
        self.cells_MNE = []
        self.cells_MNF = []
        
        self.cells_IaE = []
        self.cells_IaF = []
        
        self.cells_IbE = []
        self.cells_IbF = []
        
        self.cells_RE = []
        self.cells_RF = []
        r = 50 # Radius of cell locations from origin (0,0,0) in microns
        N = self._N
        for i in range(N):
            # Create and position cells
            _MNE = Motoneuron()
            _MNE.set_position(0, -2*r, i*r)
            self.cells.append(_MNE)
            self.cells_MNE.append(_MNE)
            
            _MNF = Motoneuron()
            _MNF.set_position(0, 2*r, i*r)
            self.cells.append(_MNF)
            self.cells_MNF.append(_MNF)
            
            _IaE = Ia_in()
            _IaE.set_position(-r, -2*r, i*r)
            self.cells.append(_IaE)
            self.cells_IaE.append(_IaE)
            
            _IaF = Ia_in()
            _IaF.set_position(-r, 2*r, i*r)
            self.cells.append(_IaF)
            self.cells_IaF.append(_IaF)
            
            _IbE = Ib_in()
            _IbE.set_position(-2*r, -2*r, i*r)
            self.cells.append(_IbE)
            self.cells_IbE.append(_IbE)
            
            _IbF = Ib_in()
            _IbF.set_position(-2*r, 2*r, i*r)
            self.cells.append(_IbF)
            self.cells_IbF.append(_IbF)
            
            _RE = Renshaw()
            _RE.set_position(r, -r, i*r)
            self.cells.append(_RE)
            self.cells_RE.append(_RE)
            
            _RF = Renshaw()
            _RF.set_position(r, r, i*r)
            self.cells.append(_RF)
            self.cells_RF.append(_RF)
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
        self.iaf_fiber_list = []
        self.iae_fiber_list = []
        self.iie_fiber_list = []
        self.iif_fiber_list = []
        self.ibe_fiber_list = []
        self.ibf_fiber_list = []
        
        for i in range(N):
            iaf = h.NetStim()
            iaf.interval = 100
            iaf.number = 1e9
            iaf.start = 0
            iaf.noise = 0.5
            self.iaf_fiber_list.append(iaf)
            
            iae = h.NetStim()
            iae.interval = 100
            iae.number = 1e9
            iae.start = 0
            iae.noise = 0.5
            self.iae_fiber_list.append(iae)
            
            iie = h.NetStim()
            iie.interval = 1000
            iie.number = 1e9
            iie.start = 0
            iie.noise = 0.5
            self.iie_fiber_list.append(iie)
            
            iif = h.NetStim()
            iif.interval = 1000
            iif.number = 1e9
            iif.start = 0
            iif.noise = 0.5
            self.iif_fiber_list.append(iif)
            
            ibe = h.NetStim()
            ibe.interval = 50
            ibe.number = 1e9
            ibe.start = 0
            ibe.noise = 0.5
            self.ibe_fiber_list.append(ibe)
            
            ibf = h.NetStim()
            ibf.interval = 50
            ibf.number = 1e9
            ibf.start = 0
            ibf.noise = 0.5
            self.ibf_fiber_list.append(ibf)
        
        
        numpy.random.seed(123)
        p = 50e-2
        syn_weight = 5e-3
        for i in range(N): 
            Y_iaf_ia = numpy.random.binomial(1, p, N) # 5% probability Ia fiber
                                                      # to Ia interneuron connection
            Y_iae_ia = numpy.random.binomial(1, p, N) # 5% probability Ia fiber
                                                      # to Ia interneuron connection
            Y_iaf_ib = numpy.random.binomial(1, p, N) # 5% probability Ia fiber
                                                      # to Ib interneuron connection
            Y_iae_ib = numpy.random.binomial(1, p, N) # 5% probability Ia fiber
                                                      # to Ib interneuron connection
            Y_iaf_mn = numpy.random.binomial(1, p, N) # 5% probability Ia fiber
                                                      # to motoneuron connection
            Y_iae_mn = numpy.random.binomial(1, p, N) # 5% probability Ia fiber
                                                      # to motoneuron connection
            
            Y_ibf_ib = numpy.random.binomial(1, p, N) # 5% probability Ib fiber
                                                      # to Ib interneuron connection
            Y_ibe_ib = numpy.random.binomial(1, p, N) # 5% probability Ib fiber
                                                      # to Ib interneuron connection         
            for k in range(N):
                if Y_iaf_ia[k]:
                    ncstim = h.NetCon(self.iaf_fiber_list[k],\
                     self.cells_IaF[i].synlist[0]) #ex
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                if Y_iae_ia[k]:
                    ncstim = h.NetCon(self.iae_fiber_list[k],\
                     self.cells_IaE[i].synlist[0]) #ex
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                if Y_iaf_ib[k]:
                    ncstim = h.NetCon(self.iaf_fiber_list[k],\
                     self.cells_IbF[i].synlist[0]) #ex
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                if Y_iae_ib[k]:
                    ncstim = h.NetCon(self.iae_fiber_list[k],\
                     self.cells_IbE[i].synlist[0]) #ex
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                if Y_iaf_mn[k]:
                    ncstim = h.NetCon(self.iaf_fiber_list[k],\
                     self.cells_MNF[i].synlist[0]) #ex
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                if Y_iae_mn[k]:
                    ncstim = h.NetCon(self.iae_fiber_list[k],\
                     self.cells_MNE[i].synlist[0]) #ex
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                    
                if Y_ibf_ib[k]:
                    ncstim = h.NetCon(self.ibf_fiber_list[k],\
                     self.cells_IbF[i].synlist[0]) #ex
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
                if Y_ibe_ib[k]:
                    ncstim = h.NetCon(self.ibe_fiber_list[k],\
                     self.cells_IbE[i].synlist[0]) #ex
                    ncstim.delay = 0
                    ncstim.weight[0] = syn_weight
                    self.nclist.append(ncstim)
            
            for i in range(len(self.nclist)):
                self.nclist[i].record(self.t_vec, self.id_vec, i)
    #
    def get_spikes(self):
        """Get the spikes as a list of lists."""
        return spiketrain.netconvecs_to_listoflists(self.t_vec, self.id_vec)