#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import zmq, pdb
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as pyplot
import mujoco2py_pb2 as mj2py
import scipy.io as sio
from helper_functions import *

enable_plotting = 1

if enable_plotting:
    # Enlarge font size
    matplotlib.rcParams.update({'font.size': 20})

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")
mat_contents = sio.loadmat("E:\\Google Drive\\Github\\tempdata\\Biomechanical Model\\data\\kinematics_bip_Array_Q19_20131126.mat") # move to fnc

all_kin = mat_contents['bip_kin'] # move to fnc
trials = range(7,20) # move to fnc
#trials = [7,8]

sitenames, target = get_kin('CORR', trials)

sitenames =    ['right_hip',  'right_knee',   'right_ankle', 'right_toe'] #move to fnc
sitenames, target = get_kin('CORR', trials)

site2mat_y  =  [8,            10,             12,            14] # move to fnc
site2mat_z  =  [9,            11,             13,            15] # move to fnc

N = 16
forces = [[] for i in range(N)]
joint_forces = [[] for i in range(6)]
site_ypos = [[] for i in range(4)]
site_zpos = [[] for i in range (4)]
target_ypos = [[] for i in range(4)]
target_zpos = [[] for i in range (4)]

in_msg = mj2py.mujoco_msg()
#total_num_items = 0
total_num_samples = 0

for a in range(len(trials)):
    current_trial = trials[a] # move to fnc
    trial = all_kin[0,current_trial] # move to fnc

    angle_trace_deg = [trial[1,:],     trial[2,:],     trial[3,:]]

    # num_items = trial[0,:].size # replace with below
    num_samples = len(target[a][0]['ypos'])

    # total_num_items += num_items # replace with below
    total_num_samples += num_samples

    # x = np.linspace(1,num_items, num_items) # replace with below
    x = np.linspace(1, num_samples, num_samples)


    #pdb.set_trace()
    #for b in range(num_items):
    for b in range(num_samples):

        #  Wait for next request from client
        message = socket.recv()

        in_msg.ParseFromString(message)
        for c in range(N):
            forces[c].append(in_msg.act[c].force)
            #print("Force[%d] = %f" % (c, in_msg.act[c].force))
            #print("Force[%d] = %f" % (c, forces[c][-1]))
        for c in range(6):
            joint_forces[c].append(in_msg.joint[c].force)

        for c in range(4):
            site_ypos[c].append(in_msg.site[c].y)
            site_zpos[c].append(in_msg.site[c].z)
        #  Send reply back to client
        out_msg = mj2py.mujoco_msg()

        for c in range(4):
            site = out_msg.site.add()

            site.name = sitenames[c]
            site.x = -0.03143
            #site.y = trial[site2mat_y[c],:][b]-trial[8,:][b] # replace with below
            site.y = target[a][c]['ypos'][b]-target[a][0]['ypos'][b]
            target_ypos[c].append(site.y)
            #site.z = trial[site2mat_z[c],:][b]-trial[9,:][b]
            site.z = target[a][c]['zpos'][b]-target[a][0]['zpos'][b]
            target_zpos[c].append(site.z)
            #print("%f: site %s to x: %f y: %f" % (c, sitenames[c], site.y, site.x))

        out_msg_str = out_msg.SerializeToString()
        socket.send(out_msg_str)
        #print(" ")

# Plotting
# pdb.set_trace()
if enable_plotting:
    fig1, axarr1 = pyplot.subplots(6, sharex=True)
    fig1.set_size_inches(6,15)
    fig2, axarr2 = pyplot.subplots(N, sharex=True)
    fig2.set_size_inches(12,30)
    fig3, axarr3 = pyplot.subplots(3, sharex=True)
    fig3.set_size_inches(6,15)
    fig4, axarr4 = pyplot.subplots(3)
    fig4.set_size_inches(6,15)

    time = np.array(range(len(joint_forces[0])))*0.01
    for a in range(6):
        axarr1[a].plot(time, joint_forces[a], 'k-') # Returns a tuple of line objects, thus the comma
        axarr1[a].set_title(in_msg.joint[a].name)
        pyplot.setp(axarr1[a].get_yticklabels(), visible=False)
        for label in axarr1[a].get_yticklabels()[0::3]:
            label.set_visible(True)
    axarr1[5].set_xlabel("Time (msec)")
    fig1.text(0.02, 0.5, 'Torque ($N\cdot m$)', va='center', rotation='vertical')

    for a in range(N):
        time = np.array(range(len(forces[a])))*0.01
        axarr2[a].plot(time, forces[a], 'k-') # Returns a tuple of line objects, thus the comma
        axarr2[a].set_title(in_msg.act[a].name)
        pyplot.setp(axarr2[a].get_yticklabels(), visible=False)
        for label in axarr2[a].get_yticklabels()[0::3]:
            label.set_visible(True)
    axarr2[N-1].set_xlabel("Time (msec)")
    fig2.text(0.02, 0.5, 'Force (N)', va='center', rotation='vertical')

    for a in range(1,4):
        time = np.array(range(len(site_ypos[a])))*0.01
        line1, = axarr3[a-1].plot(time, site_ypos[a], 'r--') # Returns a tuple of line objects, thus the comma
        line1.set_label("Computed Y position")
        line2, = axarr3[a-1].plot(time, target_ypos[a], 'r-') # Returns a tuple of line objects, thus the comma
        line2.set_label("Experimental Y position")
        line3, = axarr3[a-1].plot(time, site_zpos[a], 'b--') # Returns a tuple of line objects, thus the comma
        line3.set_label("Computed Z position")
        line4, = axarr3[a-1].plot(time, target_zpos[a], 'b-') # Returns a tuple of line objects, thus the comma
        line4.set_label("Experimental Z position")

        line5, = axarr4[a-1].plot(site_ypos[a], site_zpos[a], 'r--')
        line5.set_label("Computed YZ trajectory")

        axarr3[a-1].set_title(in_msg.site[a].name)
        axarr4[a-1].set_title(in_msg.site[a].name)
        box = axarr3[a-1].get_position()
        axarr3[a-1].set_position([box.x0, box.y0, box.width * 0.8, box.height])
        pyplot.setp(axarr3[a-1].get_yticklabels(), visible=False)

        for label in axarr3[a-1].get_yticklabels()[0::3]:
            label.set_visible(True)

    axarr3[2].set_xlabel("Time (msec)")
    fig3.text(0.02, 0.5, 'Position (m)', va='center', rotation='vertical')
    axarr3[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))

    axarr4[2].set_xlabel("Z position (cm)")
    fig4.text(0.02, 0.5, 'Y Position (m)', va='center', rotation='vertical')
    axarr4[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))

#fig1.savefig("joint_forces.png", bbox_inches='tight')
#fig2.savefig("forces.png", bbox_inches='tight')
#fig3.savefig("fits.png", bbox_inches='tight')
#fig4.savefig("trajectories.png", bbox_inches='tight')

pyplot.show()
print("total_num_items = %d" % total_num_items)
input("Please click enter to continue")
