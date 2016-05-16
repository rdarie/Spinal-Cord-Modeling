# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 18:15:40 2016

@author: Radu
"""
import struct
from neuron import h

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
