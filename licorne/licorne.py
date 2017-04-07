from PyQt5 import QtCore, QtWidgets, uic
import sys

Ui_MainWindow, QtBaseClass = uic.loadUiType('ui/MainWindow.ui')

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

