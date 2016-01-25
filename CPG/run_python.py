from neuron import h,gui
from CPG_Network import ReflexNetwork
#h.load_file('stdgui.hoc')

rc = ReflexNetwork()
shape_window = h.PlotShape()
shape_window.exec_menu('Show Diam')