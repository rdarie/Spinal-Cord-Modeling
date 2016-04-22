from neuron import h
from cell_template import Cell
import helper_functions as hf

class Mn(Cell):  #### Inherits from Cell
    """Motoneuron"""
    #### __init__ is gone and handled in Cell.
    #### We can override __init__ completely, or do some of
    #### our own initialization first, and then let Cell do its
    #### thing, and then do a bit more ourselves with "super".
    ####
    from Mn_geometry_output3 import shape_3D

    def __init__(self):
        self.d_lambda = 0.1
        self.soma = []
        self.dend = []
        self.ndend = 0
        super(Mn, self).__init__()
    #
    def create_sections(self):
        self.soma = h.Section(name = 'soma', cell = self)
        self.dend = [h.Section(name = 'dend_%d' % x, cell = self) for x in range(249)]
        self.ndend = len(self.dend)

        self.all.append(sec=self.soma)
        for a in range(self.ndend):
            self.all.append(sec=self.dend[a])
    #
    def build_topology(self):
        """Connect the sections of the cell to build a tree."""
        # Happens in shape_3D for the motor neuron

    def build_subsets(self):
        """Build subset lists. """
    #
    def define_geometry(self):
        """Set the 3D geometry of the cell."""
        self.shape_3D()
    #
    def define_biophysics(self):
        """Assign the membrane properties across the cell."""

        self.soma.insert("motoneuron")

        for dend in self.dend:
            dend.nseg = 11
            dend.Ra = 200
            dend.cm = 2
            dend.insert("pas")

    def create_synapses(self):
        """Add an exponentially decaying synapse in the middle
        of the dendrite. Set its tau to 2ms, and append this
        synapse to the synlist of the cell."""
        syn = h.ExpSyn(self.dend[0](0.1))
        syn.tau = 3
        self.synlist.append(syn) # synlist is defined in Cell

        syn = h.ExpSyn(self.dend[5](0.1))
        syn.tau = 3
        self.synlist.append(syn) # synlist is defined in Cell

        syn = h.Exp2Syn(self.soma(0.3))
        syn.tau1 = 3
        syn.tau2 = 10
        syn.e = -85
        self.synlist.append(syn) # synlist is defined in Cell

        syn = h.Exp2Syn(self.soma(0.5))
        syn.tau1 = 3
        syn.tau2 = 10
        syn.e = -85
        self.synlist.append(syn) # synlist is defined in Cell
