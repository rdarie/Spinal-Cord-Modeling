# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 08:49:01 2016

@author: Radu
"""

from neuron import h

class Motoneuron(object):
    """Two-section cell: A soma with active channels and
    a dendrite with passive properties."""
    def __init__(self):
        self.x = self.y = self.z = 0
        
        hoc_file = "..\\mn_geometries\\burke_mn_2 - Copy"
        hoc_command = "{xopen(" + hoc_command + ")}"
        h(hoc_command)
        
        self.build_topology()
        self.build_subsets()
        self.define_geometry()
        self.define_biophysics()
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
        self.soma.L = 35           # microns
        self.soma.diam = 25        # microns
        self.dend.L = 35           # microns
        self.dend.diam = 1         # microns
        self.dend.nseg = 5
        self.shape_3D()    #### Was h.define_shape(), now we do it.
    #
    def define_biophysics(self):
        """Assign the membrane properties across the cell."""
        for sec in self.all:              # 'all' exists in parent object.
            sec.Ra = 70                   # Axial resistance in Ohm * cm
            sec.cm = 1                    # Membrane capacitance in micro Farads / cm^2
        # Insert active Hodgkin-Huxley current in the soma
        
        self.soma.insert('motoneuron')
        #self.soma.gcaN_motoneuron = 0.025
        #self.soma.gcaL_motoneuron = 5e-5
        #self.soma.gcak_motoneuron = 0.15
        #self.soma.gnabar_motoneuron = 0.01
        #self.soma.gkrect_motoneuron = 0.1
        #self.soma.gl_motoneuron = 0.003
        
        #self.soma.insert('HH2new')
        #self.soma.gnabar_HH2new = 0
        #self.soma.gkbar_HH2new = 0
        
        #self.soma.insert('pas')
        #self.soma.g_pas = 1e-3       # Passive conductance in S/cm2
        #self.soma.e_pas = -64         # Leak reversal potential mV

        #self.soma.insert('extracellular')    
        
        # Insert passive current in the dendrite
        self.dend.insert('pas')
        self.dend.g_pas = 0.001         # Passive conductance in S/cm2
        self.dend.e_pas = -54.3         # Leak reversal potential mV
    #
    def build_subsets(self):
        """Build subset lists. For now we define 'all'."""
        self.all = h.SectionList()
        self.all.wholetree(sec=self.soma)
    #
    #### NEW STUFF ADDED ####
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
    def set_position(self, x, y, z):
        """
        Set the base location in 3D and move all other
        parts of the cell relative to that location.
        """
        for sec in self.all:
            # note: iterating like this changes the context for all NEURON
            # functions that depend on a section, so no need to specify sec=
            for i in range(int(h.n3d())):
                h.pt3dchange(i,
                        x - self.x + h.x3d(i),
                        y - self.y + h.y3d(i),
                        z - self.z + h.z3d(i),
                        h.diam3d(i))
        self.x, self.y, self.z = x, y, z
    #
    def rotateZ(self, theta):
        """Rotate the cell about the Z axis."""
        for sec in self.all:
            for i in range(2):
                x = h.x3d(i) * sin(theta) + h.y3d(i) * cos(theta)
                y = h.x3d(i) * cos(theta) + h.y3d(i) * -sin(theta)
                h.pt3dchange(i, x, y, h.z3d(i), h.diam3d(i))