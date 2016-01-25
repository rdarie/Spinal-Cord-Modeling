# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 10:34:07 2016

@author: Radu
"""
from cell import Cell
from neuron import h

class ClarkeRelay(Cell):  #### Inherits from Cell
    """Two-section cell: A soma with active channels and
    a dendrite with passive properties."""
    #### __init__ is gone and handled in Cell.
    #### We can override __init__ completely, or do some of
    #### our own initialization first, and then let Cell do its
    #### thing, and then do a bit more ourselves with "super".
    ####
    #### def __init__(self):
    ####     # Do some stuff
    ####     super(Cell, self).__init__()
    ####     # Do some more stuff
    #
    def create_sections(self):
        """Create the sections of the cell."""
        self.soma = h.Section(name='soma', cell=self)
        self.dend = h.Section(name='dend', cell=self)
    #
    def build_topology(self):
        """Connect the sections of the cell to build a tree."""
        self.dend.connect(self.soma(1))
    #
    def define_geometry(self):
        """Set the 3D geometry of the cell."""
        
        self.soma.L = 35                            # microns
        self.soma.diam = 25                         # microns
        
        self.dend.L = 400                           # microns
        self.dend.diam = 1                          # microns
        
        self.dend.nseg = 9
        
        self.shape_3D()
    #
    def define_biophysics(self):
        """Assign the membrane properties across the cell."""
        for sec in self.all:              # 'all' exists in parent object.
            sec.Ra = 70                   # Axial resistance in Ohm * cm
            sec.cm = 1                    # Membrane capacitance in micro Farads / cm^2
        # Insert active Hodgkin-Huxley current in the soma
        
        self.dap_syn_ = h.Exp2Syn(self.soma(0.5))
        self.dap_syn_.tau1 = 2
        self.dap_syn_.tau2 = 5
        self.dap_syn_.e = 50
        
        self.dap_nc_ = h.NetCon(self.soma(0.5)._ref_v,\
            self.dap_syn_, sec=self.soma)
        self.dap_nc_.delay = 0
        self.dap_nc_.threshold = 10
        
        self.soma.insert('clarke')
        
        self.soma.gl_clarke = 0.003
        self.soma.tau_n_bar_clarke = 7
        self.dap_nc_.weight[0] = 7.5e-3 
        self.soma.gkrect_clarke = 0.6 
        
        self.soma.insert('extracellular')    
        
        # Insert passive current in the dendrite
        self.dend.insert('pas')
        self.dend.g_pas = 0.001         # Passive conductance in S/cm2
        self.dend.e_pas = -54.3         # Leak reversal potential mV
    #
    def shape_3D(self):
        """
        Set the default shape of the cell in 3D coordinates.
        Set soma(0) to the origin (0,0,0) and dend extending along
        the X-axis.
        """
        len1 = self.soma.L
        h.pt3dclear(sec=self.soma)
        h.pt3dadd(0, 0, 0, self.soma.diam, sec=self.soma)
        h.pt3dadd(len1, 0, 0, self.soma.diam, sec=self.soma)
        len2 = self.dend.L
        h.pt3dclear(sec=self.dend)
        h.pt3dadd(len1, 0, 0, self.dend.diam, sec=self.dend)
        h.pt3dadd(len1 + len2, 0, 0, self.dend.diam, sec=self.dend)
    #
    #### build_subsets, rotateZ, and set_location are gone. ####
    #
    #### NEW STUFF ####
    #
    def create_synapses(self):
        """
        """
        self.syn_I= h.ExpSyn(self.dend(0.4))
        self.syn_I.tau = 17
        self.syn_I.e = 0
        self.synlist.append(self.syn_I)
        
        self.syn_I_inh= h.ExpSyn(self.dend(0.4))
        self.syn_I_inh.tau = 5
        self.syn_I_inh.e = -70
        self.synlist.append(self.syn_I_inh)
        
        self.syn_II= h.ExpSyn(self.dend(0.8))
        self.syn_II.tau = 18
        self.syn_II.e = 0
        self.synlist.append(self.syn_II) # synlist is defined in Cell