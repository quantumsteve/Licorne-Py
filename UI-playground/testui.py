# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layerselector.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_layerselector(object):
    def setupUi(self, layerselector):
        layerselector.setObjectName("layerselector")
        layerselector.resize(115, 404)
        self.verticalLayout = QtWidgets.QVBoxLayout(layerselector)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listView = QtWidgets.QListView(layerselector)
        self.listView.setObjectName("listView")
        self.verticalLayout.addWidget(self.listView)
        self.del_button = QtWidgets.QPushButton(layerselector)
        self.del_button.setObjectName("del_button")
        self.verticalLayout.addWidget(self.del_button)
        self.add_button = QtWidgets.QPushButton(layerselector)
        self.add_button.setObjectName("add_button")
        self.verticalLayout.addWidget(self.add_button)
        self.select_label = QtWidgets.QLabel(layerselector)
        self.select_label.setObjectName("select_label")
        self.verticalLayout.addWidget(self.select_label)
        self.select_lineEdit = QtWidgets.QLineEdit(layerselector)
        self.select_lineEdit.setObjectName("select_lineEdit")
        self.verticalLayout.addWidget(self.select_lineEdit)

        self.retranslateUi(layerselector)
        self.add_button.clicked.connect(layerselector.addClicked)
        self.del_button.clicked.connect(layerselector.delClicked)
        self.select_lineEdit.returnPressed.connect(layerselector.selectionEntered)
        QtCore.QMetaObject.connectSlotsByName(layerselector)

    def retranslateUi(self, layerselector):
        _translate = QtCore.QCoreApplication.translate
        layerselector.setWindowTitle(_translate("layerselector", "Form"))
        self.del_button.setText(_translate("layerselector", "-"))
        self.add_button.setText(_translate("layerselector", "+"))
        self.select_label.setToolTip(_translate("layerselector", "Python style range selector"))
        self.select_label.setText(_translate("layerselector", "Select:"))
        self.select_lineEdit.setToolTip(_translate("layerselector", "Python style range selector"))

