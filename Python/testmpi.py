# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 16:08:59 2016

@author: Radu
"""

from mpi4py import MPI
from neuron import h
pc = h.ParallelContext()
id = int(pc.id())
nhost = int(pc.nhost())
print "I am", id, "of", nhost