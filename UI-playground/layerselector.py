from __future__ import (absolute_import, division, print_function)
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from layer import Layer, MSLD

try:
    from PyQt5.QtCore import QString
except ImportError:
    QString = type("")


class layerselector(QtWidgets.QWidget):
    def __init__(self, sample,*args):
        QtWidgets.QWidget.__init__(self, *args)
        self.sample=sample
        self.listmodel = MyListModel(self.sample, self)
        self.listview = QtWidgets.QListView()
        self.listview.setModel(self.listmodel)
        self.listview.setSelectionMode(QtWidgets.QListView.MultiSelection)
        self.listview.selectionModel().selectionChanged.connect(self.selChanged)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.listview)
        add_button = QtWidgets.QPushButton("+")
        add_button.clicked.connect(self.addClicked)
        del_button = QtWidgets.QPushButton("-")
        del_button.clicked.connect(self.delClicked)
        prn_button = QtWidgets.QPushButton("Print")
        prn_button.clicked.connect(self.prnClicked)
        layout.addWidget(add_button)
        layout.addWidget(del_button)
        layout.addWidget(prn_button)
        self.setLayout(layout)
        
    def selChanged(self,selected,deselected):
        inds=sorted([s.row() for s in self.listview.selectionModel().selectedRows()])
        for i in inds:
            print(i)
    
    def addClicked(self):
        inds=sorted([s.row() for s in self.listview.selectionModel().selectedRows()])
        if inds:
            for i in inds:
                print('Adding ',i)
        else:
            print("add empty layer")
            #self.listmodel.append
     
    def delClicked(self):
        inds=sorted([s.row() for s in self.listview.selectionModel().selectedRows()])
        if inds:
            for i in inds:
                print('Deleting ',i)
        else:
            print("nothing selected") 

    def prnClicked(self):
        data = self.listmodel.arraydata
        for i,l in enumerate(data):
            print('Layer {0}'.format(i))
            print(data[i]) 

class MyListModel(QtCore.QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain

    def rowCount(self, parent):
        return len(self.arraydata)

    def data(self, index, role):
        indexdata = range(len(self.arraydata))
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(indexdata[index.row()])



if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    mainForm=layerselector([Layer(),Layer(thickness=2.),Layer(nsld=2.)])
    mainForm.show()
    sys.exit(app.exec_())
