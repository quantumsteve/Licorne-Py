from __future__ import (absolute_import, division, print_function)
from PyQt5 import QtCore, QtWidgets
import sys
import numpy as np
from licorne.layer import Layer, MSLD

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.cm
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

class layerplot(QtWidgets.QWidget):
    def __init__(self, *args):
        QtWidgets.QWidget.__init__(self, *args)
        sample=[Layer(thickness=1,nsld_real=5),Layer(thickness=2.,nsld_real=3),Layer(thickness=1,nsld_real=5),Layer(nsld_real=4.,thickness=np.inf)]
        self.m = PlotCanvas(sample, self)
        self.m.move(0,0)
 
    def resizeEvent(self, event):
        self.m.setGeometry(self.rect())


class PlotCanvas(FigureCanvas):

    def __init__(self, layers, parent=None):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.data=layers
        self.variable='nsld'
        self.plot()
        self.fig.canvas.mpl_connect('pick_event', self.onpick)
 
    def onpick(self,event):
        ind=event.ind[0]
        if ind==len(self.data)-1:
            ind='substrate'
        print('picked layer {0}'.format(ind))
        return True

    def plot(self):
        layer_thick_array=np.array([l.thickness.value for l in self.data])
        layer_nsld_array =np.array([l.nsld_real.value for l in self.data])
        depth=np.zeros(len(layer_thick_array))
        depth[1:]=layer_thick_array.cumsum()[:-1]
        patches=[]
        N=len(self.data)
        for i in range(N-1):
            polygon=Polygon([[depth[i],0.],[depth[i],layer_nsld_array[i]],[depth[i+1],layer_nsld_array[i]],[depth[i+1],0]],True)
            patches.append(polygon)
        polygon=Polygon([[depth[N-1],0.],[depth[N-1],layer_nsld_array[N-1]],[depth[N-1]+1,layer_nsld_array[N-1]],[depth[N-1]+1,0]],True)
        patches.append(polygon)
        p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4, picker=True)
        colors = 100*np.random.rand(len(patches))
        p.set_array(np.array(colors))
        ax = self.figure.add_subplot(111)
        ax.add_collection(p)
        ax.set_title('NSLD')
        ax.set_xlim(np.array([0,depth[-1]])*1.2)
        ax.set_ylim(np.array([0,layer_nsld_array.max()])*1.2) #TODO allow negative
        ax.set_xlabel('Thickness')
        ax.set_ylabel('NSLD')
        self.draw()

if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    mainForm=layerplot()
    mainForm.show()
    sys.exit(app.exec_())
