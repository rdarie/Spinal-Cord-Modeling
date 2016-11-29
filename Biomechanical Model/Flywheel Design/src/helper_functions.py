import zmq, pdb
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as pyplot
import mujoco2py_pb2 as mj2py
import scipy.io as sio

def get_kin(kin_type, which_trials, filename_path = "E:\\Google Drive\\Presentations\\BME Seminar Fall 2016\\3D_Kinematics_array_format.mat"):

    mat_contents = sio.loadmat(filename_path, struct_as_record=False,squeeze_me = True)
    array = mat_contents['Array']
    all_trials = array.Trials

    #pdb.set_trace()
    matching_trials = [trial for trial in all_trials if trial.Type == kin_type]
    matching_kinematics = [trial.KIN for trial in matching_trials]
    print("%d trials match this kinematic type" % len(matching_kinematics))
    #  matching_kinematics = [trial.KIN for trial in all_trials if trial.Type == kin_type]

    target = []
    sitenames =    ['right_hip',  'right_knee',   'right_ankle', 'right_knuckle', 'right_toe']
    site_aliases = [['GT X', 'GT Y', 'GT Z'],
                    [ 'K X',  'K Y', 'K Z' ],
                    [ 'M X',  'M Y', 'M Z' ],
                    ['MT X', 'MT Y', 'MT Z'],
                    [ 'T X',  'T Y', 'T Z' ]
                    ]
    for kin in [matching_kinematics[i] for i in which_trials]:
        current_target = []
        for alias in site_aliases:
            current_target.append({
            # I am going to forget what this does before long
                'xpos':[measure.Data[np.isfinite(measure.Data)] for measure in kin if measure.name == alias[0]][0],
                'ypos':[measure.Data[np.isfinite(measure.Data)] for measure in kin if measure.name == alias[1]][0],
                'zpos':[measure.Data[np.isfinite(measure.Data)] for measure in kin if measure.name == alias[2]][0]
                })

        target.append(current_target)
        # Perhaps at this point it'd be good to check that all traces have equal length, since we deleted nans

    #pdb.set_trace()

    return sitenames, target

if __name__ == "__main__":
    trials = get_kin('CORR', range(7,20))
