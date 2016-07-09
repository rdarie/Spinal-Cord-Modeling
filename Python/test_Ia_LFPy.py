# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 14:12:00 2016

@author: Radu
"""

from neuron import h, gui
h.nrn_load_dll("E:\\Google Drive\\Github\\Spinal-Cord-Modeling\\nrnmech.dll")
from Ia_LFPy import Ia

bla = Ia(n_nodes = 43)
shape_window = h.PlotShape()
input("BLA")
