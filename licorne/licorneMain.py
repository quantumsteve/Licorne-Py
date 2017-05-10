from PyQt5 import QtWidgets, QtCore, uic
import sys
from licorne import LayerPropertiesWidget, layerselector,layer,SampleModel

Ui_MainWindow, QtBaseClass = uic.loadUiType('UI/MainWindow.ui')

class  MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,sample_model_list):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.update_model(sample_model_list)
        self.selection=[]
        self.layerselector_widget.listView.selectionModel().selectionChanged.connect(self.update_selection)
        self.layerselector_widget.listView.selectionModel().selectionChanged.connect(self.layerselector_widget.selectionChanged)
        self.layerselector_widget.sampleModelChanged[SampleModel.SampleModel].connect(self.update_model)


    def update_model(self,sample_model):
        if isinstance(sample_model,SampleModel.SampleModel):
            self.sample_model=[sample_model]
        else:
            self.sample_model=sample_model
        self.layerselector_widget.set_sample_model(self.sample_model[0])
        
        all_layers=[s for s in [self.sample_model[0].incoming_media]+
                                     self.sample_model[0].layers+
                                     [self.sample_model[0].substrate]]
                                     
        self.layer_properties_widget.set_layer_list(all_layers)
        self.selection=[]
        self.layer_properties_widget.set_selection(self.selection)
        
    def update_selection(self,selected,deselected):
        all_selected=self.layerselector_widget.listView.selectionModel().selectedRows()
        self.selection=sorted([s.row() for s in all_selected])
        self.layer_properties_widget.set_selection(self.selection)

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    sm=SampleModel.SampleModel()
    window = MainWindow([sm])
    window.show()
    sys.exit(app.exec_())
