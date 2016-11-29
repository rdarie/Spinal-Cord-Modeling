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
#mat_contents = sio.loadmat("E:\\Google Drive\\Github\\tempdata\\Biomechanical Model\\data\\kinematics_bip_Array_Q19_20131126.mat") # move to fnc

trials = [0]
sitenames, target = get_kin('TRM20', trials)

N = 16
nsites = 5
njoints = 8
forces = [[] for i in range(N)]

joint_forces = [[] for i in range(njoints)]

site_xpos = [[] for i in range(nsites) ]
site_ypos = [[] for i in range(nsites) ]
site_zpos = [[] for i in range (nsites)]

target_xpos = [[] for i in range(nsites) ]
target_ypos = [[] for i in range(nsites) ]
target_zpos = [[] for i in range (nsites)]

in_msg = mj2py.mujoco_msg()

total_num_samples = 0


for a in range(len(trials)):
    #pdb.set_trace()
    #angle_trace_deg = [trial[1,:],     trial[2,:],     trial[3,:]]

    #start_idx = 1
    #end_idx = -20
    #for idx in range(4):
    #    target[a][idx]['ypos'] = target[a][idx]['ypos'][start_idx:end_idx]
    #    target[a][idx]['zpos'] = target[a][idx]['zpos'][start_idx:end_idx]

    num_samples = len(target[a][0]['ypos'])

    total_num_samples += num_samples

    x = np.linspace(1, num_samples, num_samples)

    for b in range(num_samples):

        message = socket.recv()

        in_msg.ParseFromString(message)
        for c in range(N):
            forces[c].append(in_msg.act[c].force)
            #print("Force[%d] = %f" % (c, in_msg.act[c].force))
            #print("Force[%d] = %f" % (c, forces[c][-1]))
        for c in range(njoints):
            joint_forces[c].append(in_msg.joint[c].force)
        #pdb.set_trace()
        for c in range(nsites):
            site_xpos[c].append(in_msg.site[c].x)
            site_ypos[c].append(in_msg.site[c].y)
            site_zpos[c].append(in_msg.site[c].z)
        #  Send reply back to client
        out_msg = mj2py.mujoco_msg()

        for c in range(nsites):
            site = out_msg.site.add()

            site.name = sitenames[c]
            #site.x = -0.03143
            #pdb.set_trace()
            # The crest, in hipjoint coordinates is: -0.0240141	0.013947	-0.099572
            site.x = target[a][c]['xpos'][b]-target[a][0]['xpos'][b]-0.0240141 # crest to hip joint correction
            target_xpos[c].append(site.x)
            site.y = target[a][c]['ypos'][b]-target[a][0]['ypos'][b]+0.013947 # crest to hip joint correction
            target_ypos[c].append(site.y)
            site.z = target[a][c]['zpos'][b]-target[a][0]['zpos'][b]-0.099572 # crest to hip joint correction
            target_zpos[c].append(site.z)
            #print("%f: site %s to x: %f y: %f" % (c, sitenames[c], site.y, site.x))

        out_msg_str = out_msg.SerializeToString()
        socket.send(out_msg_str)

        #start_time = 10
        #mid_time = 60
        #end_time = 110

        #if b == start_time or b == mid_time or b == end_time:
        #    print("t = %f" % b*10)
        #    pdb.set_trace()
        #Wait for next request from client
        #print(" ")

# Plotting
# pdb.set_trace()
if enable_plotting:
    fig1, axarr1 = pyplot.subplots(njoints, sharex=True)
    fig1.set_size_inches(6,15)
    fig2, axarr2 = pyplot.subplots(N, sharex=True)
    fig2.set_size_inches(12,30)
    fig3, axarr3 = pyplot.subplots(nsites-1, sharex=True)
    fig3.set_size_inches(6,15)
    fig4, axarr4 = pyplot.subplots(nsites-1)
    fig4.set_size_inches(6,15)

    time = np.array(range(len(joint_forces[0])))*10
    for a in range(njoints):
        axarr1[a].plot(time, joint_forces[a], 'k-') # Returns a tuple of line objects, thus the comma
        axarr1[a].set_title(in_msg.joint[a].name)
        pyplot.setp(axarr1[a].get_yticklabels(), visible=False)
        for label in axarr1[a].get_yticklabels()[0::3]:
            label.set_visible(True)
    axarr1[5].set_xlabel("Time (msec)")
    fig1.text(0.02, 0.5, 'Torque ($N\cdot m$)', va='center', rotation='vertical')

    for a in range(N):
        time = np.array(range(len(forces[a])))*10
        axarr2[a].plot(time, forces[a], 'k-') # Returns a tuple of line objects, thus the comma
        axarr2[a].set_title(in_msg.act[a].name)
        pyplot.setp(axarr2[a].get_yticklabels(), visible=False)
        for label in axarr2[a].get_yticklabels()[0::3]:
            label.set_visible(True)
    axarr2[N-1].set_xlabel("Time (msec)")
    fig2.text(0.02, 0.5, 'Force (N)', va='center', rotation='vertical')

    for a in range(1,5):
        time = np.array(range(len(site_ypos[a])))*10
        line1, = axarr3[a-1].plot(time, site_xpos[a], 'g--') # Returns a tuple of line objects, thus the comma
        line1.set_label("Computed X position")
        line2, = axarr3[a-1].plot(time, target_xpos[a], 'g-') # Returns a tuple of line objects, thus the comma
        line2.set_label("Experimental X position")
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
print("total_num_samples = %d" % total_num_samples)
input("Please click enter to continue")
