from helper_functions import get_af_from_mat
from matplotlib import pyplot as plt

af = get_af_from_mat('E:\\Google Drive\\Github\\tempdata\\move_root_um_move_root_points_cs.mat')

plt.figure()
plt.plot(af)

plt.show()
