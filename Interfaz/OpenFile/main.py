from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.ui = uic.loadUi('INTERFAZCNC.ui', self)
        
        self.ui.openButton.clicked.connect(self.openFile)
        self.ui.readButton.clicked.connect(self.readFile)
        
    def openFile(self):
        self.fileName = QFileDialog.getOpenFileName(self, "Open file", "/santi/Downloads", 
                                                "*.gcode, *.ngc")[0]
        self.ui.lineEdit.setText(self.fileName)
        
    def readFile(self):
        f = open(self.fileName)
        for l in f:
            print(l.strip()) 

if __name__ == "__main__": 
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()
