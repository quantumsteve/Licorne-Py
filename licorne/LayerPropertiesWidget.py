from PyQt5 import QtWidgets, QtCore, uic
import sys
from licorne import NumericParameter
import numpy as np
from collections import Iterable

Ui_LayerProperties, QtBaseClass = uic.loadUiType('UI/LayerPropertiesWidget.ui')


class LayerPropertiesWidget(QtWidgets.QWidget, Ui_LayerProperties):
    def __init__(self,layers=None,*args):
        QtWidgets.QWidget.__init__(self,*args)
        Ui_LayerProperties.__init__(self)
        self.setupUi(self)


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LayerPropertiesWidget()
    window.show()
    sys.exit(app.exec_())
