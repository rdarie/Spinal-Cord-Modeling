from neuron import h
from mycell_LFPy import my_cell
import helper_functions as hf

class Ia(my_cell):  #### Inherits from Cell
    """Ia afferent fiber"""
    #### __init__ is gone and handled in Cell.
    #### We can override __init__ completely, or do some of
    #### our own initialization first, and then let Cell do its
    #### thing, and then do a bit more ourselves with "super".
    ####
    from Ia_geometry_output import shape_3D as Ia_shape

    def __init__(self, *args, **kwargs):
        self.morphology_address = 'E:\\Google Drive\\Github\\Spinal-Cord-Modeling\\Python\\Ia_geometry_output.py'
        self.n_nodes =kwargs.pop('n_nodes')
        kwargs.update({'delete_sections' : False})
        kwargs.update({'pt3d' : True})
        kwargs.update({'morphology' : self.morphology_address})
        super(Ia, self).__init__(*args, **kwargs)

    #
    def create_sections(self):
        self.Ia_node = [h.Section(name='Ia_node_%d' % i, cell=self) for i in range(int(self.n_nodes))]
        self.Ia_paranode = [h.Section(name='Ia_paranode_%d' % i, cell=self) for i in range(int(self.n_nodes))]
    #

    def _create_sectionlists(self):
            '''Create section lists for different kinds of sections'''
            #list with all sections
            self.allsecnames = []
            self.allseclist = h.SectionList()
            for sec in h.allsec():
                if sec.name().find('Ia_') >= 0:
                    self.allsecnames.append(sec.name())
                    self.allseclist.append(sec=sec)

            #list of soma sections, assuming it is named on the format "soma*"
            self.nsomasec = 0
            self.somalist = h.SectionList()
            for sec in h.allsec():
                if sec.name().find('Ia_soma') >= 0:
                    self.somalist.append(sec=sec)
                    self.nsomasec += 1

    def build_topology(self):
        """Connect the sections of the cell to build a tree."""
        for a in range(int(self.n_nodes)):
            self.Ia_node[a].connect(self.Ia_paranode[a])
            if a < (self.n_nodes - 1):
                self.Ia_paranode[a].connect(self.Ia_node[a+1])
    #
    def define_biophysics(self):
        """Assign the membrane properties across the cell."""
        for a in range(int(self.n_nodes)): # 'all' exists in parent object.
            self.Ia_node[a].insert("axnode")

    def build_subsets(self):
        """Build subset lists. """
    #### NEW STUFF ####
    #
    def create_synapses(self):
        """Add an exponentially decaying synapse in the middle
        of the dendrite. Set its tau to 2ms, and append this
        synapse to the synlist of the cell."""
        #syn = h.ExpSyn(self.dend(0.5))
        #syn.tau = 2
        #self.synlist.append(syn) # synlist is defined in Cell
