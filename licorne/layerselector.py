from PyQt5 import QtWidgets, QtCore, uic
import sys
from licorne import SampleModel,layer

Ui_layerselector, QtBaseClass = uic.loadUiType('UI/layerselector.ui')

class layerselector(QtWidgets.QWidget, Ui_layerselector):
    invalidSelection=QtCore.pyqtSignal(str)
    def __init__(self,sample_model,*args):
        QtWidgets.QWidget.__init__(self,*args)
        Ui_layerselector.__init__(self)
        self.setupUi(self)
        self.sample_model=sample_model
        self.sample_model.setParent(self)
        self.listView.setModel(self.sample_model)
        self.listView.selectionModel().selectionChanged.connect(self.selectionChanged)
        self.invalidSelection[str].connect(self.select_label.setText)

    def addClicked(self):
        pass
        '''
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
        '''
    def delClicked(self):
        inds=sorted([s.row() for s in self.listView.selectionModel().selectedRows()], reverse=True)
        if inds:
            if inds in [[0],[self.sample_model.rowCount()-1]]:
                print('Cannot delete substrate or incoming media')
            else:
                for i in inds:
                    self.sample_model.delItem(i-1)
        else:
            print("nothing selected")
            
    def selectionEntered(self):
        selection_string=str(self.select_lineEdit.text())
        selection_string_parts=selection_string.split(',')
        selection_slices=[]
        for part in selection_string_parts:
            slice_parts=[part.split(':')
            if len(slice_parts)>3:
                self.invalidSelection.emit(part+" has more than three arguments")
                return
                
            else:
                try:
                    slice_temp=[int(x) if x.strip()!='' else None for x in slice_parts]
                    if slice_temp[1] is None and slice_temp[2] is none
                    selection_slices.append(s)
                except ValueError:
                    self.invalidSelection.emit(part+' cannot be converted to a slice')
                    return
        self.listView.selectionModel().clear()
        
        
    def selectionChanged(self,selected,deselected):
        incoming_media_index=self.sample_model.index(0)
        substrate_index=self.sample_model.index(self.sample_model.rowCount()-1)
        all_rows=self.listView.selectionModel().selectedRows()
        if (substrate_index in all_rows) and len(all_rows)>1:
            if substrate_index in selected:
                if len(selected)>1:
                    self.listView.selectionModel().select(substrate_index,QtCore.QItemSelectionModel.Deselect)
                else:
                    self.listView.selectionModel().clear()
                    self.listView.selectionModel().select(substrate_index,QtCore.QItemSelectionModel.Select)             
            else:
                self.listView.selectionModel().select(substrate_index,QtCore.QItemSelectionModel.Deselect)
        if (incoming_media_index in all_rows) and len(all_rows)>1:
            if incoming_media_index in selected:
                if len(selected)>1:
                    self.listView.selectionModel().select(incoming_media_index,QtCore.QItemSelectionModel.Deselect)
                else:
                    self.listView.selectionModel().clear()
                    self.listView.selectionModel().select(incoming_media_index,QtCore.QItemSelectionModel.Select)             
            else:
                self.listView.selectionModel().select(incoming_media_index,QtCore.QItemSelectionModel.Deselect)


if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    sm=SampleModel.SampleModel()
    sm.addItem(layer.Layer(name='0'))
    sm.addItem(layer.Layer(name='1'))
    sm.addItem(layer.Layer(name='2'))
    sm.addItem(layer.Layer(name='3'))
    window = layerselector(sm)
    window.show()
    sys.exit(app.exec_())

