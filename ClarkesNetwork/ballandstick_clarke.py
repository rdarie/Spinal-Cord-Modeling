# -*- coding: utf-8 -*-
"""
Created on Thu Jan 07 11:09:10 2016

@author: Radu
"""

from neuron import h
from math import sin, cos
import numpy

class BallAndStick(object):
    """Two-section cell: A soma with active channels and
    a dendrite with passive properties."""
    def __init__(self):
        self.x = self.y = self.z = 0
        self.create_sections()
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

        #self.soma.L = 35*25                          # microns
        #self.soma.diam = 1                           # microns
        
        #g_pas_equiv = 2e-3
        self.soma.L = 35                            # microns
        self.soma.diam = 25                         # microns
        
        self.dend.L = 350                           # microns
        self.dend.diam = 1                          # microns
        
        self.dend.nseg = 9
        
        #lambda_dc = 50*numpy.sqrt(self.soma.diam/g_pas_equiv/self.soma.Ra)
        #self.dend.L = self.dend.nseg*lambda_dc/(self.dend.nseg + self.soma.nseg)
        #self.soma.L = self.soma.nseg*lambda_dc/(self.dend.nseg + self.soma.nseg)
        
        self.shape_3D()    #### Was h.define_shape(), now we do it.
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

        self.dend_syn= h.Exp2Syn(self.dend(0.5))
        self.dend_syn.tau1 = 2
        self.dend_syn.tau2 = 5
        self.dend_syn.e = 0
        
        self.soma.insert('clarke')
        # FINAL VERSIONS
        self.soma.gl_clarke = 0.003
        self.soma.tau_n_bar_clarke = 7
        self.dap_nc_.weight[0] = 7.5e-3 
        self.soma.gkrect_clarke = 0.6 
        
        # SWEEP VALUES
        #self.soma.gcaN_clarke      = 0
        #self.soma.gcaL_clarke      = 0
        #self.soma.gcak_clarke      = 0
        #self.soma.gnapbar_clarke   = 0
        #self.soma.tau_mc_clarke    = 0
        #self.soma.tau_hc_clarke    = 0
        #self.soma.tau_n_bar_clarke = 0
        #self.dap_nc_.weight[0]     = 0
        #self.soma.gkrect_clarke    = 0 
        #self.soma.gnabar_clarke    = 0
        
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