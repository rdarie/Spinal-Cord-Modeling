from neuron import h
from cell_template import Cell, lambda_f
import helper_functions as hf

class Ia(Cell):  #### Inherits from Cell
    """Ia afferent fiber"""
    #### __init__ is gone and handled in Cell.
    #### We can override __init__ completely, or do some of
    #### our own initialization first, and then let Cell do its
    #### thing, and then do a bit more ourselves with "super".
    ####
    from Ia_geometry_output import shape_3D

    def __init__(self):
         self.sim_params = hf.get_net_params(hf.get_tempdata_address())
         self.n_nodes = self.sim_params[0][0]
         self.diameter = self.sim_params[4][0]
         self.inl = self.sim_params[5][0]
         self.length = self.sim_params[4][0]
         self.d_lambda = 0.1
         super(Ia, self).__init__()
    #
    def create_sections(self):

        self.Ia_node = [h.Section(name='node_%d' % i, cell=self) for i in range(int(self.n_nodes))]
        self.Ia_paranode = [h.Section(name='paranode_%d' % i, cell=self) for i in range(int(self.n_nodes))]

        for a in range(int(self.n_nodes)):
            self.all.append(sec=self.Ia_node[a])
            self.all.append(sec=self.Ia_paranode[a])
    #
    def build_topology(self):
        """Connect the sections of the cell to build a tree."""
        for a in range(int(self.n_nodes)):
            self.Ia_node[a].connect(self.Ia_paranode[a])
            if a < (self.n_nodes - 1):
                self.Ia_paranode[a].connect(self.Ia_node[a+1])

    #
    def define_geometry(self):
        """Set the 3D geometry of the cell."""

        for a in range(int(self.n_nodes)):
            self.Ia_node[a].L = self.length
            self.Ia_paranode[a].L = self.length * self.inl

            self.Ia_node[a].diam = self.diameter
            self.Ia_paranode[a].diam = self.diameter

            self.Ia_node[a].nseg = int((self.Ia_node[a].L/(self.d_lambda*lambda_f(self.Ia_node[a], 100))+0.9)/2)*2 + 1
            self.Ia_paranode[a].nseg = int((self.Ia_paranode[a].L/(self.d_lambda*lambda_f(self.Ia_node[a], 100))+0.9)/2)*2 + 1
        #self.soma.L = self.soma.diam = 12.6157 # microns
        #self.dend.L = 200                      # microns
        #self.dend.diam = 1                     # microns
        #self.dend.nseg = 5
        self.shape_3D()
    #
    def define_biophysics(self):
        """Assign the membrane properties across the cell."""
        base_Ra = 70

        for a in range(int(self.n_nodes)): # 'all' exists in parent object.
            self.Ia_node[a].insert("axnode")
            self.Ia_node[a].insert("extracellular")
            self.Ia_node[a].Ra = base_Ra    # Axial resistance in Ohm * cm
            self.Ia_node[a].cm = 2      # Membrane capacitance in micro Farads / cm^2

            self.Ia_paranode[a].insert("pas")
            self.Ia_paranode[a].insert("extracellular")
            self.Ia_paranode[a].Ra = base_Ra    # Axial resistance in Ohm * cm
            self.Ia_paranode[a].cm = 2            # Membrane capacitance in micro Farads / cm^2
        # Insert active Hodgkin-Huxley current in the soma
        #self.soma.insert('hh')
        #self.soma.gnabar_hh = 0.12  # Sodium conductance in S/cm2
        #self.soma.gkbar_hh = 0.036  # Potassium conductance in S/cm2
        #self.soma.gl_hh = 0.0003    # Leak conductance in S/cm2
        #self.soma.el_hh = -54.3     # Reversal potential in mV
        # Insert passive current in the dendrite
        #self.dend.insert('pas')
        #self.dend.g_pas = 0.001  # Passive conductance in S/cm2
        #self.dend.e_pas = -65    # Leak reversal potential mV
    #
    #def shape_3D(self):
#        """
#        Set the default shape of the cell in 3D coordinates.
#        Set soma(0) to the origin (0,0,0) and dend extending along
#        the X-axis.
#        """
        #len1 = self.soma.L
        #h.pt3dclear(sec=self.soma)
        #h.pt3dadd(0, 0, 0, self.soma.diam, sec=self.soma)
        #h.pt3dadd(len1, 0, 0, self.soma.diam, sec=self.soma)
        #len2 = self.dend.L
        #h.pt3dclear(sec=self.dend)
        #h.pt3dadd(len1, 0, 0, self.dend.diam, sec=self.dend)
        #h.pt3dadd(len1 + len2, 0, 0, self.dend.diam, sec=self.dend)
    #
    #### build_subsets, rotateZ, and set_location are gone. ####

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
