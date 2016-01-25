# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 09:41:53 2016

@author: Radu
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 10:34:07 2016

@author: Radu
"""

import sys
sys.path.insert(0, '../ClarkesNetwork')

from cell import Cell
from neuron import h

class Motoneuron(Cell):  #### Inherits from Cell
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
        
        self.soma.L = 1                             # microns
        self.soma.diam = 1                          # microns
        
        self.dend.L = 1                             # microns
        self.dend.diam = 1                          # microns
        
        self.dend.nseg = 9
        
        self.shape_3D()
    #
    def define_biophysics(self):
        """Assign the membrane properties across the cell."""
        for sec in self.all:              # 'all' exists in parent object.
            sec.Ra = 70                   # Axial resistance in Ohm * cm
            sec.cm = 1                    # Membrane capacitance in micro Farads / cm^2
            
            sec.insert('motoneuron')
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
        """
        """
        syn_ = h.ExpSynR(self.soma(0.5))
        syn_.tau = 5
        syn_.e = -10
        self.synlist.append(syn_)
        
        syn_ = h.ExpSynR(self.soma(0.5))
        syn_.tau = 5
        syn_.e = -70
        self.synlist.append(syn_)