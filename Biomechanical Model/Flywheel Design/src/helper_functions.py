import zmq, pdb
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as pyplot
import mujoco2py_pb2 as mj2py
import scipy.io as sio

def get_kin(kin_type, which_trials, filename_path = "A:\\Array files\\Newer Arrays\\Array_Q19_Merged.mat"):

    mat_contents = sio.loadmat(filename_path, struct_as_record=False,squeeze_me = True)
    array = mat_contents['Array']
    all_trials = array.Trials

    matching_trials = [trial for trial in all_trials if trial.Type == kin_type]
    matching_kinematics = [trial.KIN for trial in matching_trials]
    #  matching_kinematics = [trial.KIN for trial in all_trials if trial.Type == kin_type]

    target = []
    sitenames =    ['right_hip',  'right_knee',   'right_ankle', 'right_toe']
    for kin in matching_kinematics:
        hip_y   = [measure.Data for measure in kin if measure.name == 'GT Y'][0]
        hip_z   = [measure.Data for measure in kin if measure.name == 'GT Z'][0]
        knee_y  = [measure.Data for measure in kin if measure.name == 'K Y'][0]
        knee_z  = [measure.Data for measure in kin if measure.name == 'K Z'][0]
        ankle_y = [measure.Data for measure in kin if measure.name == 'M Y'][0]
        ankle_z = [measure.Data for measure in kin if measure.name == 'M Z'][0]
        toe_y = [measure.Data for measure in kin if measure.name == 'MT Y'][0]
        toe_z = [measure.Data for measure in kin if measure.name == 'MT Z'][0]

        target.append([{'ypos':hip_y, 'zpos':hip_z},{'ypos':knee_y, 'zpos':knee_z},
            {'ypos':ankle_y, 'zpos':ankle_z},{'ypos':toe_y, 'zpos':toe_z}])

    #pdb.set_trace()

    return sitenames, target

if __name__ == "__main__":
    trials = get_kin('CORR', range(7,20))
