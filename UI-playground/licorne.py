from __future__ import (absolute_import, division, print_function)
import sys
from PyQt4 import QtGui
from . import licorneGUI

def qapp():
    if QtGui.QApplication.instance():
        _app = QtGui.QApplication.instance()
    else:
        _app = QtGui.QApplication(sys.argv)
    return _app

if __name__ == '__main__':
    app = qapp()
    main_window = licorneGUI.licorneGUI()
    main_window.show()
    sys.exit(app.exec_())

