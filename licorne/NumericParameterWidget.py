from PyQt5 import QtWidgets, QtCore, uic
import sys
from licorne import NumericParameter
import numpy as np
from collections import Iterable


Ui_NumericParameter, QtBaseClass = uic.loadUiType('UI/NumericParameterWidget.ui')

class NumericParameterWidget(QtWidgets.QWidget, Ui_NumericParameter):
    def __init__(self,*args,parameter=None,available_ties=None):
        QtWidgets.QWidget.__init__(self,*args)
        Ui_NumericParameter.__init__(self)
        self.setupUi(self)
        self.parameter=parameter
        self.available_ties=available_ties
        if self.parameter is not None:
            self.updateUiFromParameter(parameter,available_ties)

    def updateUiFromParameter(self,parameter,available_ties):
        print(parameter)
        self.ties_comboBox.addItem('')
        if isinstance(available_ties,str):
            self.ties_comboBox.addItem(available_ties)
        elif isinstance(available_ties,Iterable):
            for ties in available_ties:
                self.ties_comboBox.addItem(ties)
        else:
            pass #None case or some weird input
        if isinstance(parameter,NumericParameter.NumericParameter):
            self.value_lineEdit.setText(str(parameter.value))
            self.unchanged_radioButton.setEnabled(False)
            try:
                tie_index=available_ties.index(parameter.expr)+1
            except:
                tie_index=0
            self.ties_comboBox.setCurrentIndex(tie_index)
            if parameter.vary:
                self.fit_radioButton.setChecked(True)
                self.add_current_tie(parameter,available_ties)
            else:
                self.fixed_radioButton.setChecked(True)
            if parameter.minimum==-np.inf:
                self.minimum_lineEdit.setText('')
            else:
                self.minimum_lineEdit.setText(str(parameter.minimum))
            if parameter.maximum==np.inf:
                self.maximum_lineEdit.setText('')
            else:
                self.maximum_lineEdit.setText(str(parameter.maximum))
        else:
            self.updateUiFromParameter(parameter[0],available_ties)
            self.ties_comboBox.insertItem(1,'Mixed/Unchanged')
            if len(set((p.expr for p in parameter)))!=1:
                self.ties_comboBox.setCurrentIndex(1)
            if len(set((p.value for p in parameter)))!=1:
                self.value_lineEdit.setText(str(parameter[0].value)+' multiple')
            if len(set((p.vary for p in parameter)))!=1:
                self.unchanged_radioButton.setChecked(True)
            if len(set((p.minimum for p in parameter)))!=1:
                self.minimum_lineEdit.setText(str(parameter[0].minimum)+' multiple')
            if len(set((p.maximum for p in parameter)))!=1:
                self.maximum_lineEdit.setText(str(parameter[0].maximum)+' multiple')
        
    def add_current_tie(self,parameter,available_ties):
        '''
        parameter : NumericParameter (cannot be Iterable)
        '''
        name=parameter.name
        if self.fit_radioButton.isChecked() and self.ties_comboBox.findText(name)==-1:
            self.ties_comboBox.addItem(name)

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    par1=NumericParameter.NumericParameter(name='par1',value=3,maximum=7,vary=True,expr='other value1')
    par2=NumericParameter.NumericParameter(name='par2',value=3,maximum=7,vary=True)
    par3=NumericParameter.NumericParameter(name='par3',value=3,vary=False)
    window = NumericParameterWidget(parameter=[par1,par2,par3],available_ties=['other value','different value'])
    window.show()
    sys.exit(app.exec_())
