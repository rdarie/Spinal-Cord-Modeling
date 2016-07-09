from neuron import h
from mycell_LFPy import my_cell
import helper_functions as hf
import pdb

class Mn(my_cell):  #### Inherits from Cell
    """Motoneuron"""
    #### __init__ is gone and handled in Cell.
    #### We can override __init__ completely, or do some of
    #### our own initialization first, and then let Cell do its
    #### thing, and then do a bit more ourselves with "super".
    ####

    def __init__(self, *args, **kwargs):
        self.morphology_address = 'E:\\Google Drive\\Github\\Spinal-Cord-Modeling\\mn_geometries\\burke_mn_2_postparser.py'
        kwargs.update({'delete_sections' : False})
        kwargs.update({'pt3d' : True})
        kwargs.update({'morphology' : self.morphology_address})
        super(Mn, self).__init__(*args, **kwargs)
    #
    def create_sections(self):
    	self.soma = [h.Section(name = 'Mn_soma', cell = self)]
    	self.dend = [h.Section(name = 'Mn_dend_%d' % x, cell = self) for x in range(351)]
        self.ndend = len(self.dend)
    #
    def _create_sectionlists(self):
            '''Create section lists for different kinds of sections'''
            #list with all sections
            self.allsecnames = []
            self.allseclist = h.SectionList()
            for sec in h.allsec():
                if sec.name().find('Mn_') >= 0:
                    self.allsecnames.append(sec.name())
                    self.allseclist.append(sec=sec)

            #list of soma sections, assuming it is named on the format "soma*"
            self.nsomasec = 0
            self.somalist = h.SectionList()
            for sec in h.allsec():
                if sec.name().find('Mn_soma') >= 0:
                    #pdb.set_trace()
                    self.somalist.append(sec=sec)
                    self.nsomasec += 1

    def build_topology(self):
        """Connect the sections of the cell to build a tree."""
        # Happens in shape_3D for the motor neuron
    #
    def define_biophysics(self):
        """Assign the membrane properties across the cell."""
        self.soma[0].insert("motoneuron")

    def build_subsets(self):
        """Build subset lists. """
    #### NEW STUFF ####
    #
    def create_synapses(self):
        #pdb.set_trace()
        """Add an exponentially decaying synapse in the middle
        of the dendrite. Set its tau to 2ms, and append this
        synapse to the synlist of the cell."""
        synapseParameters = {
        'idx' : self.get_idx(section='Mn_soma')[0],   # insert synapse on index "0", the soma
        'e' : 0.,                                     # reversal potential of synapse
        'syntype' : 'ExpSyn',   # conductance based double-exponential synapse
        'tau' : 2.0,            # Time constant
        'weight' : 0.002,        # Synaptic weight
        'record_current' : True,# disable synapse current recording
        }
        self.set_synapse(**synapseParameters)
