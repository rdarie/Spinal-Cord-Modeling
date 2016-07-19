from neuron import h
from mycell_LFPy import my_cell
import helper_functions as hf
import pdb

class Clarke(my_cell):  #### Inherits from Cell
    """Clarke Interneuron"""
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
        super(Clarke, self).__init__(*args, **kwargs)
    #
    def create_sections(self):
    	self.soma = [h.Section(name = 'Clarke_soma', cell = self)]
        self.dend = [h.Section(name = 'Clarke_dend', cell=self)]
        self.ndend = 1

        self.shape_3D()

    #
    def _create_sectionlists(self):
            '''Create section lists for different kinds of sections'''
            #list with all sections
            self.allsecnames = []
            self.allseclist = h.SectionList()
            for sec in h.allsec():
                if sec.name().find('Clarke_') >= 0:
                    self.allsecnames.append(sec.name())
                    self.allseclist.append(sec=sec)

            #list of soma sections, assuming it is named on the format "soma*"
            self.nsomasec = 0
            self.somalist = h.SectionList()
            for sec in h.allsec():
                if sec.name().find('Clarke_soma') >= 0:
                    #pdb.set_trace()
                    self.somalist.append(sec=sec)
                    self.nsomasec += 1

    def build_topology(self):
        """Connect the sections of the cell to build a tree."""
        self.dend[0].connect(self.soma[0](1))
    #
    def define_biophysics(self):
        """Assign the membrane properties across the cell."""

        self.soma[0].L = 35                            # microns
        self.soma[0].diam = 25                         # microns

        self.dend[0].L = 40                           # microns
        self.dend[0].diam = 1                          # microns

        self.dend[0].nseg = 1
        self.dap_syn_ = h.Exp2Syn(self.soma[0](0.5))
        self.dap_syn_.tau1 = 2
        self.dap_syn_.tau2 = 5
        self.dap_syn_.e = 50

        self.dap_nc_ = h.NetCon(self.soma[0](0.5)._ref_v,\
            self.dap_syn_, sec=self.soma[0])
        self.dap_nc_.delay = 0
        self.dap_nc_.threshold = 10

        self.soma[0].insert('clarke')

        self.soma[0].gl_clarke = 0.003
        self.soma[0].tau_n_bar_clarke = 7
        self.dap_nc_.weight[0] = 7.5e-3
        self.soma[0].gkrect_clarke = 0.6


        # Insert passive current in the dendrite
        self.dend[0].insert('pas')
        self.dend[0].g_pas = 0.001         # Passive conductance in S/cm2
        self.dend[0].e_pas = -54.3         # Leak reversal potential mV

    def shape_3D(self):
        """
        Set the default shape of the cell in 3D coordinates.
        Set soma(0) to the origin (0,0,0) and dend extending along
        the X-axis.
        """
        len1 = self.soma[0].L
        h.pt3dclear(sec=self.soma[0])
        h.pt3dadd(0, 0, 0, self.soma[0].diam, sec=self.soma[0])
        h.pt3dadd(len1, 0, 0, self.soma[0].diam, sec=self.soma[0])
        len2 = self.dend[0].L
        h.pt3dclear(sec=self.dend[0])
        h.pt3dadd(len1, 0, 0, self.dend[0].diam, sec=self.dend[0])
        h.pt3dadd(len1 + len2, 0, 0, self.dend[0].diam, sec=self.dend[0])
#
    def build_subsets(self):
        """Build subset lists. """
    #### NEW STUFF ####
    #
    def create_synapses(self):
        """Build subset lists. """
        #pdb.set_trace()
        synapseParameters_E0 = {
        'idx' : self.get_idx()[1],   # insert synapse on index "0", the soma
        'e' : -10.,                                     # reversal potential of synapse
        'syntype' : 'ExpSyn',   # conductance based double-exponential synapse
        'tau' : 5.0,            # Time constant
        'weight' : 0.5,        # Synaptic weight
        'record_current' : True,# disable synapse current recording
        }
        self.set_synapse(**synapseParameters_E0)
