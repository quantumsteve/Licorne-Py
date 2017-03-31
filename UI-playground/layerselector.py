from __future__ import (absolute_import, division, print_function)
from PyQt5 import QtCore, QtWidgets
import sys
import numpy as np
from layer import Layer, MSLD

class layerselector(QtWidgets.QWidget):
    def __init__(self, sample,*args):
        QtWidgets.QWidget.__init__(self, *args)
        self.listmodel = MyListModel(sample, self)
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
        substrate_index=self.listmodel.index(len(self.listmodel.arraydata)-1)
        all_rows=self.listview.selectionModel().selectedRows()
        if (substrate_index in all_rows) and len(all_rows)>1:
            if substrate_index in selected:
                if len(selected)>1:
                    self.listview.selectionModel().select(substrate_index,QtCore.QItemSelectionModel.Deselect)
                else:
                    self.listview.selectionModel().clear()
                    self.listview.selectionModel().select(substrate_index,QtCore.QItemSelectionModel.Select)
            else:
                self.listview.selectionModel().select(substrate_index,QtCore.QItemSelectionModel.Deselect) 

    def addClicked(self):
        inds=sorted([s.row() for s in self.listview.selectionModel().selectedRows()])
        if inds:
            for i in inds:
                if i!= len(self.listmodel.arraydata)-1:
                    print('Adding ',i)
                    self.listmodel.addItem(self.listmodel.arraydata[i])
                else:
                    print('Cannot add substrate')
        else:
            print("add empty layer")
            self.listmodel.addItem(Layer())

    def delClicked(self):
        inds=sorted([s.row() for s in self.listview.selectionModel().selectedRows()], reverse=True)
        if inds:
            for i in inds:
                if i!= len(self.listmodel.arraydata)-1:
                    print('Deleting ',i)
                    self.listmodel.delItem(i)
                else:
                    print('Cannot delete substrate')
        else:
            print("nothing selected") 

    def prnClicked(self):
        data = self.listmodel.arraydata
        for i,l in enumerate(data):
            print('Layer {0}'.format(i))
            print(l)


class MyListModel(QtCore.QAbstractListModel):

    def __init__(self, datain, parent=None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain

    def rowCount(self, parent=None):
        return len(self.arraydata)

    def data(self, index, role):
        indexdata = range(len(self.arraydata))
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        if index.row()==len(self.arraydata)-1:
            return QtCore.QVariant('substrate')
        return QtCore.QVariant(indexdata[index.row()])

    def addItem(self,item):
        position=len(self.arraydata)-1
        self.beginInsertRows(QtCore.QModelIndex(), position, position)
        self.arraydata.insert(position, item)
        self.endInsertRows()

    def delItem(self,position):
        if position!=self.rowCount()-1:
            self.beginRemoveRows(QtCore.QModelIndex(), position, position)
            del self.arraydata[position]
            self.endRemoveRows()
        else:
            print('Cannot remove substrate')

if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    mainForm=layerselector([Layer(),Layer(thickness=2.),Layer(nsld=2.,thickness=np.inf)])
    mainForm.show()
    sys.exit(app.exec_())
