# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 18:15:40 2016

@author: Radu
"""
import struct, pdb
from neuron import h
import cPickle as pickle
from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def get_net_params(tempdata_address):

    text_file_location = tempdata_address + "cell_params"
    result = []
    text_file = open(text_file_location, 'rb')

    value = text_file.read(8)
    while value:
        result.append(struct.unpack("d",value))
        value = text_file.read(8)
    #print result
    #print len(result)
    text_file.close()
    return result

def get_tempdata_address(double_escaped = 0):
    h('systype = unix_mac_pc()')

    if h.systype == 3:
        if double_escaped:
            tempdata_address = '..\\\\..\\\\tempdata\\\\'
        else:
            tempdata_address = '..\\..\\tempdata\\'
    else:
        tempdata_address = "../tempdata/"

    return tempdata_address

def get_mn_geom_address(double_escaped = 0):
    h('systype = unix_mac_pc()')

    if h.systype == 3:
        if double_escaped:
            mn_geom_address = '..\\\\mn_geometries\\\\'
        else:
            mn_geom_address = '..\\mn_geometries\\'
    else:
        mn_geom_address = "mn_geometries/"

    return mn_geom_address

def get_comsol_voltage(tempdata_address):

    text_file_location = tempdata_address + "matlab_v_extra"
    result = []
    text_file = open(text_file_location, 'rb')

    value = text_file.read(8)
    while value:
        result.append(struct.unpack("d",value))
        value = text_file.read(8)
    text_file.close()
    return result

def plot_fiber_voltage(filename):

    data = pickle.load( open(filename, "rb" ) )

    decimate_s = 10
    decimate_t = 100
    nproc = len(data)
    data_plot = []
    ddata2dx2 = []
    ddata2dx2_plot = []
    dx = 1
    dt = 1
    for proc in range(len(data)):
        data_plot.append(data[proc]['iav'][::decimate_s, ::decimate_t])
        #pdb.set_trace()
        ddata2dx2.append(np.gradient(data[proc]['iav'],dx, axis = 1))
        ddata2dx2_plot.append(ddata2dx2[proc][::decimate_s, ::decimate_t])

    nseg, nsamp = ddata2dx2_plot[0].shape
    x = np.arange(nsamp)
    y = np.arange(nseg)
    X,Y = np.meshgrid(x, y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(X, Y, ddata2dx2_plot[0], rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    plt.show()
    pdb.set_trace()
