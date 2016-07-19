# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 18:15:40 2016

@author: Radu
"""
import struct, pdb, collections
from neuron import h
import cPickle as pickle
from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import scipy, scipy.signal
import scipy.io as sio
from math import sqrt

from mayavi import mlab

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
        result.append(struct.unpack("d",value)[0])
        value = text_file.read(8)
    text_file.close()
    return result

def square_wave(t):
    pdb.set_trace()
    ret_val = scipy.signal.square(2 * np.pi * t * 1e-3 * 10, duty = 0.2)
    if isinstance(ret_val, collections.Iterable):
        ret_val[t<100] = 0
    else:
        if t < 100:
            ret_val = 0
    return ret_val

def sine_wave(t):
    ret_val = np.sin(2 * np.pi * t * 1e-3 * 10)
    if isinstance(ret_val, collections.Iterable):
        ret_val[t<100] = 0
    else:
        if t < 100:
            ret_val = 0
    return ret_val

def plot_fiber_location_voltage(filename,nameout,stim_func,fibertype, location):

    data = pickle.load( open(filename, "rb" ) )

    # decimate data for plotting
    decimate_t = 1
    nproc = len(data)
    ia_plot = []
    #mn_plot = []
    t_plot = []
    #pdb.set_trace()
    t_plot.append(data[0]['tvec'][::decimate_t])
    #

    for proc in range(len(data)):
        #pdb.set_trace()
        ia_plot.append(data[proc][fibertype][location, ::decimate_t])
        #mn_plot.append(data[proc]['somav'][::decimate_t])

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ia_plot, = ax.plot(t_plot[0], ia_plot[0], label = 'Membrane voltage of axon terminal')
    #mn_plot, = ax.plot(t_plot[0], mn_plot[0], label = 'Membrane voltage of motoneuron soma')
    stim_plot, = ax.plot(t_plot[0], stim_func(t_plot[0]), label = 'Stimulus waveform')
    plt.xlabel('Time (msec)')
    plt.ylabel('Membrane Voltage (mV)')
    ax.legend(handles=[ia_plot, stim_plot])
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width, box.height * 0.8])

    # Put a legend to the right of the current axis
    lgd = ax.legend(loc='upper center', bbox_to_anchor=(0., 1.02, 1., .102))
    plt.show()
    fig.savefig(nameout + '.png', dpi=300, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')

def plot_fiberandcell_location_voltage(filename,whatcell, cell_shorthand,nameout,stim_func,fibertype, location):

    data = pickle.load( open(filename, "rb" ) )

    # decimate data for plotting
    decimate_t = 1
    nproc = len(data)
    ia_plot = []
    mn_plot = []
    t_plot = []
    #pdb.set_trace()
    t_plot.append(data[0]['tvec'][::decimate_t])
    #

    for proc in range(len(data)):
        #pdb.set_trace()
        ia_plot.append(data[proc][fibertype][location, ::decimate_t])
        mn_plot.append(data[proc][cell_shorthand][::decimate_t])

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ia_plot, = ax.plot(t_plot[0], ia_plot[0], label = 'Membrane voltage of axon terminal')
    mn_plot, = ax.plot(t_plot[0], mn_plot[0], label = 'Membrane voltage of ' + whatcell)
    stim_plot, = ax.plot(t_plot[0], stim_func(t_plot[0]), label = 'Stimulus waveform')
    plt.xlabel('Time (msec)')
    plt.ylabel('Membrane Voltage (mV)')
    ax.legend(handles=[ia_plot,mn_plot, stim_plot])
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width, box.height * 0.8])

    # Put a legend to the right of the current axis
    lgd = ax.legend(loc='upper center', bbox_to_anchor=(0., 1.02, 1., .102))
    plt.show()
    fig.savefig(nameout + '.png', dpi=300, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')

def plot_fiber_voltage_distribution(filename,fibertype, timepoint):

    data = pickle.load( open(filename, "rb" ) )

    # decimate data for plotting
    decimate_s = 1
    nproc = len(data)
    ia_plot = []

    for proc in range(len(data)):
        #pdb.set_trace()
        ia_plot.append(data[proc][fibertype][::decimate_s, timepoint])

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(ia_plot[0])
    plt.show()

def plot_fiber_voltage(filename,fibertype):

    data = pickle.load( open(filename, "rb" ) )

    decimate_s = 1
    decimate_t = 1
    nproc = len(data)
    data_plot = []
    ddata2dx2 = []
    ddata2dx2_plot = []
    dx = 1
    dt = 1
    for proc in range(len(data)):
        data_plot.append(data[proc][fibertype][::decimate_s, ::decimate_t])
        ddata2dx2.append(np.gradient(data[proc][fibertype],dx))
        ddata2dx2_plot.append(ddata2dx2[proc][0][::decimate_t, ::decimate_s])

    nseg, nsamp = ddata2dx2_plot[0].shape
    x = np.arange(nseg)

    t_plot = []
    t_plot.append(data[0]['tvec'][::decimate_t])
    y = t_plot[0]

    X,Y = np.meshgrid(x, y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    mlab.figure(1, fgcolor=(0, 0, 0), bgcolor=(1, 1, 1))

    s = mlab.surf(data_plot[0], warp_scale="auto", extent = [0,1,0,5,0,1])
    #pdb.set_trace()
    ax=mlab.axes(s, ranges = [0, 43.306, np.min(y), np.max(y), np.min(data_plot[0]), np.max(data_plot[0])])
    #
    ax.axes.label_format='%.2f'
    ax.label_text_property.font_family = 'arial'
    mlab.xlabel('Distance along axon (mm)')
    mlab.ylabel('Time (msec)')
    mlab.zlabel('Membrane voltage (mV)')

    ax.axes.font_factor=0.9
    mlab.savefig('3d_voltage.png', size=(1920, 1080))
    #pdb.set_trace()
    bla = input()
    #plt.show()
    #pdb.set_trace()

def get_af_from_mat(filename, which):
    mat_contents = sio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    sim_struct = mat_contents['simulation']

    nrows, ncols = sim_struct[which].d2V_ds2.shape

    d2V_ds2_mag = []

    for a in range(ncols):
        d2V_ds2_mag.append(sqrt(pow(sim_struct[which].d2V_ds2[0,a],2)
        +pow(sim_struct[which].d2V_ds2[1,a],2)+pow(sim_struct[which].d2V_ds2[2,a],2)))

    return d2V_ds2_mag

def plot_af_from_mat(filename, which):
    af = get_af_from_mat(filename, which)
    x = np.linspace(0,43.306,len(af))
    fig = plt.figure()
    plt.plot(x,af)
    plt.xlabel('Distance along axon (mm)')
    plt.ylabel('Activating function along axon (V/m^2)')
    plt.tight_layout()
    plt.show()
    fig.savefig('plot_af_from_mat.png', dpi=300, format='png', bbox_inches='tight')

def get_v_from_mat(filename, which):
    mat_contents = sio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    #pdb.set_trace()
    sim_struct = mat_contents['simulation']

    return sim_struct[which].V_extra

def get_n_nodes_from_mat(filename, which):
    mat_contents = sio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    #pdb.set_trace()
    sim_struct = mat_contents['simulation']

    return sim_struct[which].n_nodes

def get_dom_from_mat(filename, which):
    mat_contents = sio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    sim_struct = mat_contents['simulation']

    return sim_struct[which].domain

def get_sigma_from_mat(filename, which):
    mat_contents = sio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    sim_struct = mat_contents['simulation']

    return sim_struct[which].sigma
