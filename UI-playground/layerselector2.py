from PyQt5 import QtWidgets, uic
import sys

Ui_layerselector, QtBaseClass = uic.loadUiType('ui/layerselector2.ui')

class layerselector2(QtWidgets.QWidget, Ui_layerselector):
    def __init__(self,*args):
        QtWidgets.QWidget.__init__(self,*args)
        Ui_layerselector.__init__(self)
        self.setupUi(self)
    def addClicked(self):
        pass
    def delClicked(self):
        pass
    def selectionEntered(self):
        pass

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = layerselector2()
    window.show()
    sys.exit(app.exec_())

