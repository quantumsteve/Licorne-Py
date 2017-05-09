from PyQt5 import QtWidgets, QtCore, uic
import sys
from licorne import NumericParameter,layer,LayerList
import numpy as np
from collections import Iterable

Ui_LayerProperties, QtBaseClass = uic.loadUiType('UI/LayerPropertiesWidget.ui')


class LayerPropertiesWidget(QtWidgets.QWidget, Ui_LayerProperties):
    def __init__(self,parent=None,layers=None,selected=None,*args):
        QtWidgets.QWidget.__init__(self,parent=parent,*args)
        Ui_LayerProperties.__init__(self)
        self.setupUi(self)
        self.layer_list=[]
        self.selection=[]
        self.ties_nsld_real=[]
        self.ties_nsld_imaginary=[]
        self.ties_msld_rho=[]
        self.ties_msld_theta=[]
        self.ties_msld_phi=[]
        self.ties_roughness=[]
        if layer is not None:
            self.set_layer_list(layers)
            if selected is not None:
                self.set_selection(selected)

    def set_layer_list(self,newlist):
        self.layer_list=newlist
        self.selection=[]
        self.ties_nsld_real, self.ties_nsld_imaginary, self.ties_msld_rho, \
            self.ties_msld_theta, self.ties_msld_phi, self.ties_roughness=\
                LayerList.generate_available_ties(self.layer_list[1:-1],self.layer_list[0],self.layer_list[-1])

    def set_selection(self,selected):
        self.selection=selected
        if selected==[0]:
            prefix='Incoming_media.'
        elif selected==[len(self.layer_list)-1]:
            prefix='Substrate.'
        else:
            prefix='Layer{0}.'.format(np.min(selected))
        self.NSLDR.updateUiFromParameter([self.layer_list[x].nsld_real for x in self.selection],self.ties_nsld_real,prefix)
        self.NSLDI.updateUiFromParameter([self.layer_list[x].nsld_imaginary for x in self.selection],self.ties_nsld_imaginary,prefix)
        self.MSLD_rho.updateUiFromParameter([self.layer_list[x].msld.rho for x in self.selection],self.ties_msld_rho,prefix)
        self.MSLD_theta.updateUiFromParameter([self.layer_list[x].msld.theta for x in self.selection],self.ties_msld_theta,prefix)
        self.MSLD_phi.updateUiFromParameter([self.layer_list[x].msld.phi for x in self.selection],self.ties_msld_phi,prefix)
        self.MSLD_rho.updateUiFromParameter([self.layer_list[x].msld.rho for x in self.selection],self.ties_msld_rho,prefix)
        self.Roughness.updateUiFromParameter([self.layer_list[x].roughness for x in self.selection],self.ties_roughness,prefix)
        self.Thickness.updateUiFromParameter([self.layer_list[x].thickness for x in self.selection],self.ties_thickness,prefix)
        #TODO: rougness model and sublayers
        #TODO: name

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    l1=layer.Layer(name='layer0',nsld_real=1)
    l1.nsld_real.vary=True
    l2=layer.Layer(nsld_real=2)
    selected=[0]
    window = LayerPropertiesWidget(layers=[l1,l2],selected=selected)
    window.show()
    sys.exit(app.exec_())
