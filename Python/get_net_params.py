# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 18:15:40 2016

@author: Radu
"""
import struct

def get_net_params(tempdata_address):
    
    text_file_location = tempdata_address + "cell_params"
    result = []
    text_file = open(text_file_location, 'rb')
    
    value = text_file.read(8)
    while value:
        result.append(struct.unpack("d",value))
        value = text_file.read(8)
    print result
    print len(result)
    text_file.close()
    return result