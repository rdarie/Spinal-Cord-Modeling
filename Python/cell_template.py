import numpy as np
from neuron import h
import math

def lambda_f(section, freq):
    if h.n3d() < 2:
        return 1e5*math.sqrt(section.diam/(math.pi*4*freq*section.Ra*section.cm))
    else:
        x1 = h.arc3d(0)
        d1 = h.diam3d(0)
        lam = 0
        for i in range(int(h.n3d())):
            x2 = h.arc3d(i)
            d2 = h.diam3d(i)
            lam += (x2 - x1)/math.sqrt(d1 + d2)
            x1 = x2
            d1 = d2
        lam *=  math.sqrt(2) * 1e-5*math.sqrt(4*math.pi*freq*section.Ra*section.cm)

    return section.L / lam

class Cell(object):
    """Generic cell template."""
    def __init__(self):
        self.x, self.y, self.z = 0, 0, 0
        self.synlist = []
        self.all = h.SectionList()
        self.create_sections()
        self.build_topology()
        self.build_subsets()
        self.define_geometry()
        self.define_biophysics()
        self.create_synapses()
    #
    def create_sections(self):
        """Create the sections of the cell. Remember to do this
        in the form::
            h.Section(name='soma', cell=self)
        """
        raise NotImplementedError("create_sections() is not implemented.")
    #
    def build_topology(self):
        """Connect the sections of the cell to build a tree."""
        raise NotImplementedError("build_topology() is not implemented.")
    #
    def define_geometry(self):
        """Set the 3D geometry of the cell."""
        raise NotImplementedError("define_geometry() is not implemented.")
    #
    def define_biophysics(self):
        """Assign the membrane properties across the cell."""
        raise NotImplementedError("define_biophysics() is not implemented.")
    #
    def create_synapses(self):
        """Subclasses should create synapses (such as ExpSyn) at various
        segments and add them to self.synlist."""
        pass # Ignore if child does not implement.
    #
    def build_subsets(self):
        """Build subset lists. This defines 'all', but subclasses may
        want to define others. If overridden, call super() to include 'all'."""
        self.all.wholetree(sec=self.soma)
    #
    def connect2target(self, source_section, target, thresh=10):
        """Make a new NetCon with this cell's membrane
        potential at the soma as the source (i.e. the spike detector)
        onto the target passed in (i.e. a synapse on a cell).
        Subclasses may override with other spike detectors."""
        nc = h.NetCon(source_section(1)._ref_v, target, sec = source_section)
        nc.threshold = thresh
        return nc
    #
    def is_art(self):
        """Flag to check if we are an integrate-and-fire artificial cell."""
        return 0
    #
    def set_position(self, x, y, z):
        """
        Set the base location in 3D and move all other
        parts of the cell relative to that location.
        """
        for sec in self.all:
            sec.push()
            #print('secname = %s, h.n3d = %d' % (h.secname(), h.n3d()))
            for i in range(int(h.n3d())):
                h.pt3dchange(i,
                        x - self.x + h.x3d(i),
                        y - self.y + h.y3d(i),
                        z - self.z + h.z3d(i),
                        h.diam3d(i), sec=sec)
            h.pop_section()
        #h.define_shape()
        self.x, self.y, self.z = x, y, z
    #
    def rotateZ(self, theta):
        """Rotate the cell about the Z axis."""
        rot_m = numpy.array([[sin(theta), cos(theta)], [cos(theta), -sin(theta)]])
        for sec in self.all:
            for i in range(int(h.n3d())):
                xy = numpy.dot([h.x3d(i), h.y3d(i)], rot_m)
                h.pt3dchange(i, xy[0], xy[1], h.z3d(i), h.diam3d(i))
