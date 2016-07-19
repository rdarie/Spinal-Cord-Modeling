from neuron import h
from mycell_LFPy import my_cell
import helper_functions as hf

class Ib(my_cell):  #### Inherits from Cell
    """Ia afferent fiber"""
    #### __init__ is gone and handled in Cell.
    #### We can override __init__ completely, or do some of
    #### our own initialization first, and then let Cell do its
    #### thing, and then do a bit more ourselves with "super".
    ####
    from Ib_geometry_postparser import shape_3D as Ib_shape

    def __init__(self, *args, **kwargs):
        self.morphology_address = 'E:\\Google Drive\\Github\\Spinal-Cord-Modeling\\Python\\Ib_geometry_postparser.py'
        self.n_nodes =kwargs.pop('n_nodes')
        kwargs.update({'delete_sections' : False})
        kwargs.update({'pt3d' : True})
        kwargs.update({'morphology' : self.morphology_address})
        kwargs.update({'v_init' : -87.0 })
        super(Ib, self).__init__(*args, **kwargs)

    #
    def create_sections(self):
        self.Ib_node = [h.Section(name='Ib_node_%d' % i, cell=self) for i in range(int(self.n_nodes))]
        self.Ib_paranode = [h.Section(name='Ib_paranode_%d' % i, cell=self) for i in range(int(self.n_nodes))]
    #

    def _create_sectionlists(self):
            '''Create section lists for different kinds of sections'''
            #list with all sections
            self.allsecnames = []
            self.allseclist = h.SectionList()
            for sec in h.allsec():
                if sec.name().find('Ib_') >= 0:
                    self.allsecnames.append(sec.name())
                    self.allseclist.append(sec=sec)

            #list of soma sections, assuming it is named on the format "soma*"
            self.nsomasec = 0
            self.somalist = h.SectionList()
            for sec in h.allsec():
                if sec.name().find('Ib_soma') >= 0:
                    self.somalist.append(sec=sec)
                    self.nsomasec += 1

    def build_topology(self):
        """Connect the sections of the cell to build a tree."""
        for a in range(int(self.n_nodes)):
            self.Ib_node[a].connect(self.Ib_paranode[a])
            if a < (self.n_nodes - 1):
                self.Ib_paranode[a].connect(self.Ib_node[a+1])
    #
    def define_biophysics(self):
        """Assign the membrane properties across the cell."""
        for a in range(int(self.n_nodes)): # 'all' exists in parent object.
            self.Ib_node[a].insert("axnode")
            self.Ib_paranode[a].g_pas=0.001/(2*9.15*self.Ib_node[a].diam+2*30)
            self.Ib_paranode[a].e_pas=-80

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
