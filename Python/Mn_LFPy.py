from neuron import h
from mycell_LFPy import my_cell
import helper_functions as hf

class Mn(my_cell):  #### Inherits from Cell
    """Motoneuron"""
    #### __init__ is gone and handled in Cell.
    #### We can override __init__ completely, or do some of
    #### our own initialization first, and then let Cell do its
    #### thing, and then do a bit more ourselves with "super".
    ####

    def __init__(self, *args, **kwargs):
        self.morphology_address = 'E:\\Google Drive\\Github\\Spinal-Cord-Modeling\\Python\\Mn_geometry_output3.py'
        kwargs.update({'delete_sections' : False})
        kwargs.update({'pt3d' : True})
        kwargs.update({'morphology' : self.morphology_address})
        super(Mn, self).__init__(*args, **kwargs)
    #
    def create_sections(self):
        self.soma = h.Section(name = 'soma', cell = self)
        self.dend = [h.Section(name = 'dend_%d' % x, cell = self) for x in range(249)]
        self.ndend = len(self.dend)
    #
    def build_topology(self):
        """Connect the sections of the cell to build a tree."""
        # Happens in shape_3D for the motor neuron
    #
    def define_biophysics(self):
        """Assign the membrane properties across the cell."""
        self.soma.insert("motoneuron")

    def build_subsets(self):
        """Build subset lists. """
    #### NEW STUFF ####
    #
    def create_synapses(self):
        """Add an exponentially decaying synapse in the middle
        of the dendrite. Set its tau to 2ms, and append this
        synapse to the synlist of the cell."""
        synapseParameters = {
        'idx' : self.get_idx(section='soma')[0],               # insert synapse on index "0", the soma
        'e' : 0.,                # reversal potential of synapse
        'syntype' : 'ExpSyn',   # conductance based double-exponential synapse
        'tau' : 2.0,            # Time constant
        'weight' : 0.002,        # Synaptic weight
        'record_current' : True,# disable synapse current recording
        }
        self.set_synapse(**synapseParameters)
