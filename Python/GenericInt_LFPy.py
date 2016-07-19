from neuron import h
from mycell_LFPy import my_cell
import helper_functions as hf
import pdb

class GenericInt(my_cell):  #### Inherits from Cell
    """Generic Interneuron"""
    #### __init__ is gone and handled in Cell.
    #### We can override __init__ completely, or do some of
    #### our own initialization first, and then let Cell do its
    #### thing, and then do a bit more ourselves with "super".
    ####

    def __init__(self, *args, **kwargs):
        self.morphology_address = 'E:\\Google Drive\\Github\\Spinal-Cord-Modeling\\Python\\blank_geometry.py'
        kwargs.update({'delete_sections' : False})
        kwargs.update({'pt3d' : True})
        kwargs.update({'morphology' : self.morphology_address})
        #kwargs.update({'v_init' : -67.0 })
        super(GenericInt, self).__init__(*args, **kwargs)
    #
    def create_sections(self):
    	self.soma = h.Section(name = 'Int_soma', cell = self)
        self.dend = h.Section(name='dend', cell=self)
        self.ndend = 1

    #
    def _create_sectionlists(self):
            '''Create section lists for different kinds of sections'''
            #list with all sections
            self.allsecnames = []
            self.allseclist = h.SectionList()
            for sec in h.allsec():
                if sec.name().find('Int_') >= 0:
                    self.allsecnames.append(sec.name())
                    self.allseclist.append(sec=sec)

            #list of soma sections, assuming it is named on the format "soma*"
            self.nsomasec = 0
            self.somalist = h.SectionList()
            for sec in h.allsec():
                if sec.name().find('Int_soma') >= 0:
                    #pdb.set_trace()
                    self.somalist.append(sec=sec)
                    self.nsomasec += 1

    def build_topology(self):
        """Connect the sections of the cell to build a tree."""
        self.dend.connect(self.soma(1))
    #
    def define_biophysics(self):
        """Assign the membrane properties across the cell."""
        self.soma.insert("hh")
        self.dend.insert("pas")
    	self.soma.L = 5.64
        self.dend.L = 1
    	self.soma.diam = 5.64
        self.soma.gnabar_hh = 120 * 1e-3
        self.soma.gkbar_hh = 100 * 1e-3
        self.soma.gl_hh = 0.51 * 1e-3
        self.soma.el_hh = -64
    	self.soma.ena = 55
    	self.soma.ek = -80

    def build_subsets(self):
        """Build subset lists. """
    #### NEW STUFF ####
    #
    def create_synapses(self):
        """Build subset lists. """
    #pdb.set_trace()
    #
