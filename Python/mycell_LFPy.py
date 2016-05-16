from neuron import h
from LFPy import Cell
import imp

class my_cell(Cell):  #### Inherits from Cell
    """Generic cell template"""
    #### __init__ is gone and handled in Cell.
    #### We can override __init__ completely, or do some of
    #### our own initialization first, and then let Cell do its
    #### thing, and then do a bit more ourselves with "super".
    ####

    def __init__(self, *args, **kwargs):
    # Create and connect the sections
        self.create_sections()
        self.build_topology()

        '''        popped_kwargs = {
                    morphology,
                    v_init=-65.,
                    passive = True,
                    Ra=150,
                    rm=30000,
                    cm=1.0,
                    e_pas=-65.,
                    extracellular = True,
                    timeres_NEURON=2**-3,
                    timeres_python=2**-3,
                    tstartms=0,
                    tstopms=100,
                    nsegs_method='lambda100',
                    lambda_f = 100,
                    d_lambda = 0.1,
                    max_nsegs_length=None,
                    delete_sections = True,
                    custom_code=None,
                    custom_fun=None,
                    custom_fun_args=None,
                    pt3d=False,
                    verbose=False
        }'''
        kwargs.update({'verbose' : False})
        super(my_cell, self).__init__(*args, **kwargs)
        # Add biophysics and synapses. Note that these could be run as custom code too
        self.define_biophysics()
        self.create_synapses()
    #
    def create_sections(self):
        raise NotImplementedError("create_sections() is not implemented.")
    #
    def build_topology(self):
        """Connect the sections of the cell to build a tree."""
        raise NotImplementedError("build_topology() is not implemented.")
    #
    def define_biophysics(self):
        """Assign the membrane properties across the cell."""
        raise NotImplementedError("define_biophysics() is not implemented.")

    def build_subsets(self):
        """Build subset lists. """
    #### NEW STUFF ####
    def _load_geometry(self):
        '''Load the morphology-file in NEURON'''
        try:
            h.sec_counted = 0
        except LookupError:
            h('sec_counted = 0')

        #import the morphology, try and determine format
        fileEnding = self.morphology.split('.')[-1]
        if fileEnding == 'hoc' or fileEnding == 'HOC':
            h.load_file(1, self.morphology)
        elif fileEnding == 'py':
            geom_func = imp.load_source('shape_3D', self.morphology)
            geom_func.shape_3D(self)
        else:
            neuron.h('objref this')
            if fileEnding == 'asc' or fileEnding == 'ASC':
                Import = h.Import3d_Neurolucida3()
                if not self.verbose:
                    Import.quiet = 1
            elif fileEnding == 'swc' or fileEnding ==  'SWC':
                Import = h.Import3d_SWC_read()
            elif fileEnding == 'xml' or fileEnding ==  'XML':
                Import = h.Import3d_MorphML()
            else:
                raise ValueError('%s is not a recognised morphology file format!'
                                 ).with_traceback(
                    'Should be either .hoc, .asc, .swc, .xml!' %self.morphology)

            #assuming now that morphologies file is the correct format
            try:
                Import.input(self.morphology)
            except:
                if not hasattr(neuron, 'neuroml'):
                    raise Exception('Can not import, try and copy the ' + \
                    'nrn/share/lib/python/neuron/neuroml ' + \
                    'folder into %s' % neuron.__path__[0])
                else:
                    raise Exception('something wrong with file, see output')
            try:
                imprt = neuron.h.Import3d_GUI(Import, 0)
            except:
                raise Exception('See output, try to correct the file')
            imprt.instantiate(neuron.h.this)

        h.define_shape()
        self._create_sectionlists()

    def create_synapses(self):
        """Add an exponentially decaying synapse in the middle
        of the dendrite. Set its tau to 2ms, and append this
        synapse to the synlist of the cell."""

    def _loadspikes(self):
        '''
        LFPy defaults to external spike times for each synapse. That's unnecessary
        for our purposes (all synapses are driven by the spiking of other cells).
        Here I just override the LFPy _loadspikes() function in order to avoid
         an error message
        '''

    def connect2target(self, source_section, target, thresh=10):
        """Make a new NetCon with this cell's membrane
        potential at the soma as the source (i.e. the spike detector)
        onto the target passed in (i.e. a synapse on a cell).
        Subclasses may override with other spike detectors."""
        nc = h.NetCon(source_section(1)._ref_v, target, sec = source_section)
        nc.threshold = thresh
        return nc
