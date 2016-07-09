debugging = 1

import os, pdb
from neuron import h
if debugging:
    from neuron import gui
else:
    h.load_file('noload.hoc')

import scipy
from scipy.interpolate import interp1d

from matplotlib import pyplot as plt
from neuronpy.graphics import spikeplot
import helper_functions as hf
from Ia_network_LFPy import Ia_network as Ia_net
import numpy as np
import cPickle as pickle
from helper_functions import plot_fiber_voltage

plot_fiber_voltage("E:\\Google Drive\\Github\\tempdata\\test_net.p")
