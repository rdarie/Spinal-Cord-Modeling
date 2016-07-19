from neuron import h
from GenericInt_LFPy import GenericInt
import helper_functions as hf
import pdb

class Ren(GenericInt):  #### Inherits from Cell
    """Ia Interneuron"""
    #### __init__ is gone and handled in Cell.
    #### We can override __init__ completely, or do some of
    #### our own initialization first, and then let Cell do its
    #### thing, and then do a bit more ourselves with "super".
    ####
    def create_synapses(self):
        #pdb.set_trace()
        """Add an exponentially decaying synapse in the middle
        of the dendrite. Set its tau to 2ms, and append this
        synapse to the synlist of the cell."""
        synapseParameters_E0 = {
        'idx' : self.get_idx(section='Int_soma')[0],   # insert synapse on index "0", the soma
        'e' : -10.,                                     # reversal potential of synapse
        'syntype' : 'ExpSyn',   # conductance based double-exponential synapse
        'tau' : 5.0,            # Time constant
        'weight' : 0.5,        # Synaptic weight
        'record_current' : True,# disable synapse current recording
        }
        self.set_synapse(**synapseParameters_E0)
