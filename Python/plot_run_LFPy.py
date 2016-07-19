debugging = 1

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
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
#from Ia_network_LFPy import Ia_network as Ia_net
import numpy as np
import cPickle as pickle
from helper_functions import *

#plot_fiberandcell_location_voltage("E:\\Google Drive\\Github\\tempdata\\Clarke_net.p",'Clarke nucleus cell', 'somav','Clarke-terminal' , square_wave, 'iav', -1)
plot_fiber_location_voltage("E:\\Google Drive\\Github\\tempdata\\Ia_net_square.p",'Ia-Mn-terminal',square_wave, 'iav', -1)
plot_fiber_location_voltage("E:\\Google Drive\\Github\\tempdata\\Ia_net_sine.p",'Ib-Mn-terminal',sine_wave, 'iav', -1)
#f = plot_fiber_voltage_distribution("E:\\Google Drive\\Github\\tempdata\\iab_net.p",'ibv', 4900)
#plot_af_from_mat('E:\\Google Drive\\Github\\tempdata\\move_root_um_move_root_points_cs.mat',0)
#plot_fiber_voltage("E:\\Google Drive\\Github\\tempdata\\Ia_net.p", 'iav')
