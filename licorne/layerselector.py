from PyQt5 import QtWidgets, uic
import sys
from licorne import SampleModel

Ui_layerselector, QtBaseClass = uic.loadUiType('UI/layerselector.ui')

class layerselector(QtWidgets.QWidget, Ui_layerselector):
    def __init__(self,sm,*args):
        QtWidgets.QWidget.__init__(self,*args)
        Ui_layerselector.__init__(self)
        self.setupUi(self)
        self.listView.setModel(sm)
    def addClicked(self):
        pass
    def delClicked(self):
        pass
    def selectionEntered(self):
        pass
    def selectionChanged(self):
        print("selection changed")

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = layerselector(SampleModel.SampleModel())
    window.show()
    sys.exit(app.exec_())

