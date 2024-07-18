
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from matplotlib.pyplot import text
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
import sys
import serial
from fileinput import filename
from PyQt5.Qsci import *
import view3d
import time


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        self.ui = uic.loadUi('mainw.ui', self)
        self.view_3D = view3d.View3D()
        self.ui.viewLayout.addWidget(self.view_3D)
               
        self.ui.pushButton_7.clicked.connect(self.openFile)
        self.ui.pushButton_7.clicked.connect(self.readFile)
        

        self.ui.pushButton_8.clicked.connect(self.openSVGFile)
        self.ui.dibujar.clicked.connect(self.readFile)
        
                               
        self.__editor = QsciScintilla()
        self.ui.gridLayout.addWidget(self.__editor)


        self.ui.botonZmas.clicked.connect(self.clickZmas)
        self.ui.botonZmenos.clicked.connect(self.clickZmenos)

        self.ui.botonXmas.clicked.connect(self.clickXmas)
        self.ui.botonXmenos.clicked.connect(self.clickXmenos)

        self.ui.botonYmas.clicked.connect(self.clickYmas)
        self.ui.botonYmenos.clicked.connect(self.clickYmenos)

        self.serial = serial.Serial('COM8', 115200)
    
    def clickZmas(self):
        dataZ0="$G\n"
        dataZ1="$J=G21G91X0Y0Z1F10\n"
        self.serial.write(dataZ0.encode('utf-8'))
        self.serial.write(dataZ1.encode('utf-8'))
    
    def clickZmenos(self):
        dataZ0M="$G\n"
        dataZ1M="$J=G21G91X0Y0Z-1F10\n"
        self.serial.write(dataZ0M.encode('utf-8'))
        self.serial.write(dataZ1M.encode('utf-8'))

    def clickXmas(self):
        dataX0="$G\n"
        dataX1="$J=G21G91X1Y0Z0F10\n"
        self.serial.write(dataX0.encode('utf-8'))
        self.serial.write(dataX1.encode('utf-8'))

    def clickXmenos(self):
        dataX0M="$G\n"
        dataX1M="$J=G21G91X-1Y0Z0F10\n"
        self.serial.write(dataX0M.encode('utf-8'))
        self.serial.write(dataX1M.encode('utf-8'))
    
    def clickYmas(self):
        dataY0="$G\n"
        dataY1="$J=G21G91X0Y1Z0F10\n"
        self.serial.write(dataY0.encode('utf-8'))
        self.serial.write(dataY1.encode('utf-8'))

    def clickYmenos(self):
        dataY0M="$G\n"
        dataY1M="$J=G21G91X0Y-1Z0F10\n"
        self.serial.write(dataY0M.encode('utf-8'))
        self.serial.write(dataY1M.encode('utf-8'))
     
          
    def openFile(self):
        self.fileName = QFileDialog.getOpenFileName(self, "Open file", "/home/", 
                                                "*.gcode *.ngc")[0]
        self.ui.lineEdit.setText(self.fileName)
        self.__editor.setText(open(self.fileName).read().replace(";"," ")) 

        gcode= open(self.fileName).read().replace(";"," ") 
        self.view_3D.compute_data(gcode)
        self.view_3D.draw()       
      
    
    def readFile(self):
        f = open(self.fileName, 'r')

        self.serial.write("\n\n".encode('utf-8'))
        time.sleep(2)
        self.serial.flushInput()

        for line in f:
            l = line.strip()
            if not l.startswith('(') and not l.startswith('%'):
                print('Sending: '+ l)
                self.serial.write((l + '\n').encode('utf-8'))
                grbl_out = self.readline().decode('utf-8')
                print(': '+grbl_out.strip())

        f.close()

       
    def send_message(self, message):
        text = self.ui.textEdit.toPlainText()
        text += message + '\n'
        self.ui.textEdit.setText(text)
        data = message + '\n'
        self.serial.write(data.encode('utf-8'))
        lectura = self.serial.readline().decode('utf-8')

    

    def openSVGFile(self):

        self.fileName = QFileDialog.getOpenFileName(self, "Open file", "/home/", 
                                                "*.svg *.gcode")[0]
        
        gcode_compiler = Compiler(interfaces.Gcode, movement_speed=1000, cutting_speed=300, pass_depth=5)
        curves = parse_file(self.fileName) # Parse an svg file into geometric curves
        gcode_compiler.append_curves(curves) 
        self.fileName = self.fileName.replace(".svg",".gcode")
        gcode_compiler.compile_to_file(self.fileName, passes=2)
     

        svg = open(self.fileName).read().replace(";"," ")
        self.view_3D.compute_data(svg)
        self.view_3D.draw() 

    
                            
if __name__ == "__main__": 
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()
