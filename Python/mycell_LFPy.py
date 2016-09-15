from neuron import h
from LFPy import Cell
import imp, pdb
import numpy as np
from LFPy import RecExtElectrode
from LFPy.run_simulation import _run_simulation, _run_simulation_with_electrode
from LFPy.run_simulation import _collect_geometry_neuron
from LFPy.alias_method import alias_method

class my_cell(Cell):  #### Inherits from Cell
    """Generic cell template"""
    #### __init__ is gone and handled in Cell.
    #### We can override __init__ completely, or do some of
    #### our own initialization first, and then let Cell do its
    #### thing, and then do a bit more ourselves with "super".
    ####

    def __init__(self,is_last_in_network = False, *args,  **kwargs):
        # Create and connect the sections
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
        self.is_last_in_network = is_last_in_network
        self.create_sections()
        self.build_topology()
        #pdb.set_trace()
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

    def gather_recordings(self, rec_imem=False, rec_vmem=False,
                     rec_ipas=False, rec_icap=False,
                     rec_isyn=False, rec_vmemsyn=False, rec_istim=False,
                     rec_variables=[]):
        if rec_imem:
            self._calc_imem()
        if rec_ipas:
            self._calc_ipas()
        if rec_icap:
            self._calc_icap()
        if rec_vmem:
            self._collect_vmem()
        if rec_isyn:
            self._collect_isyn()
        if rec_vmemsyn:
            self._collect_vsyn()
        if rec_istim:
            self._collect_istim()
        if len(rec_variables) > 0:
            self._collect_rec_variables(rec_variables)
        if hasattr(self, 'netstimlist'):
            del self.netstimlist
        #somatic trace
        self.somav = np.array(self.somav)

    def simulate(self, electrode=None, rec_imem=False, rec_vmem=False,
                     rec_ipas=False, rec_icap=False,
                     rec_isyn=False, rec_vmemsyn=False, rec_istim=False,
                     rec_variables=[], variable_dt=False, atol=0.001,
                     to_memory=True, to_file=False, file_name=None,
                     dotprodcoeffs=None):
            '''
            This is the main function running the simulation of the NEURON model.
            Start NEURON simulation and record variables specified by arguments.

            Arguments:
            ::

                electrode:  Either an LFPy.RecExtElectrode object or a list of such.
                            If supplied, LFPs will be calculated at every time step
                            and accessible as electrode.LFP. If a list of objects
                            is given, accessible as electrode[0].LFP etc.
                rec_imem:   If true, segment membrane currents will be recorded
                            If no electrode argument is given, it is necessary to
                            set rec_imem=True in order to calculate LFP later on.
                            Units of (nA).
                rec_vmem:   record segment membrane voltages (mV)
                rec_ipas:   record passive segment membrane currents (nA)
                rec_icap:   record capacitive segment membrane currents (nA)
                rec_isyn:   record synaptic currents of from Synapse class (nA)
                rec_vmemsyn:    record membrane voltage of segments with Synapse(mV)
                rec_istim:  record currents of StimIntraElectrode (nA)
                rec_variables: list of variables to record, i.e arg=['cai', ]
                variable_dt: boolean, using variable timestep in NEURON
                atol:       absolute tolerance used with NEURON variable timestep
                to_memory:  only valid with electrode, store lfp in -> electrode.LFP
                to_file:    only valid with electrode, save LFPs in hdf5 file format
                file_name:  name of hdf5 file, '.h5' is appended if it doesnt exist
                dotprodcoeffs :  list of N x Nseg np.ndarray. These arrays will at
                            every timestep be multiplied by the membrane currents.
                            Presumably useful for memory efficient csd or lfp calcs
                '''
            self._set_soma_volt_recorder()
            self._collect_tvec()

            if rec_imem:
                self._set_imem_recorders()
            if rec_vmem:
                self._set_voltage_recorders()
            if rec_ipas:
                self._set_ipas_recorders()
            if rec_icap:
                self._set_icap_recorders()
            if len(rec_variables) > 0:
                self._set_variable_recorders(rec_variables)

            #run fadvance until t >= tstopms, and calculate LFP if asked for
            if self.is_last_in_network:
                if electrode is None and dotprodcoeffs is None:
                    if not rec_imem:
                        print(("rec_imem = %s, membrane currents will not be recorded!" \
                                          % str(rec_imem)))
                    _run_simulation(self, variable_dt, atol)
                else:
                    #allow using both electrode and additional coefficients:
                    _run_simulation_with_electrode(self, electrode, variable_dt, atol,
                                                       to_memory, to_file, file_name,
                                                       dotprodcoeffs)

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
