import numpy as np
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.dataQ,self.dataR,self.datadR,_,_=np.loadtxt('REF_M_24600+24601+24602+24603_Specular_++-SD-PFO30-2-20Oe.dat',unpack=True)
        self.plot()

    def plot(self):
        # instead of ax.hold(False)
        self.figure.clear()
        self.figure.patch.set_facecolor('white')
        # create an axis
        ax = self.figure.add_subplot(111)
        ax.errorbar(self.dataQ, self.dataR, yerr=self.datadR,fmt='ro' )
        ax.set_yscale('log')
        ax.grid(True,which="both")
        ax.set_xlabel('Q')
        ax.set_ylabel('Reflectivity')
        # refresh canvas
        self.canvas.draw()


if __name__=='__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
    
