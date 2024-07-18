import sys
import serial
import serial.tools.list_ports as list_ports

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QWidget
from matplotlib.pyplot import text
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces

from PyQt5.Qsci import *
import view3d
import time
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets, uic

import cv2
import pygame.camera

from PyQt5.QtWidgets import (
    QApplication, 
    QLabel,
    QPushButton, 
    QGridLayout, 
    QWidget   
)

from PIL import Image, ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

import os
from PIL import Image, ImageFilter

from time import sleep
import pygame
from PIL import Image

class ReadPort(QtCore.QObject):

    def __init__(self, serial):
        super().__init__()
        self.serial = serial
        self.running = 1

    def setFileName(self, fileName):
        self.fileName = fileName  
         

    def run(self):
        f = open(self.fileName, 'r')

        self.serial.write("\n\n".encode('utf-8'))
        time.sleep(2)
        self.serial.flushInput()

        for line in f:
            l = line.strip()
            if not l.startswith('(') and not l.startswith('%'):
                print('Sending: '+ l)
                self.serial.write((l + '\n').encode('utf-8'))
                grbl_out = self.serial.readline().decode('utf-8')
                print(': '+grbl_out.strip())
            if(self.running==0):
                return

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        self.ui = uic.loadUi('mainw.ui', self)
        self.view_3D = view3d.View3D()
        self.ui.viewLayout.addWidget(self.view_3D)
               
        self.ui.pushButton_7.clicked.connect(self.openFile)
        #self.ui.pushButton_7.clicked.connect(self.readFile)
        self.ui.camara.clicked.connect(self.showCamera)

        self.ui.pushButton_8.clicked.connect(self.openSVGFile)
        self.ui.dibujar.clicked.connect(self.play)
                                     
        self.__editor = QsciScintilla()
        self.ui.gridLayout.addWidget(self.__editor)

        self.ui.botonZmas.clicked.connect(self.clickZmas)
        self.ui.botonZmenos.clicked.connect(self.clickZmenos)

        self.ui.botonXmas.clicked.connect(self.clickXmas)
        self.ui.botonXmenos.clicked.connect(self.clickXmenos)

        self.ui.botonYmas.clicked.connect(self.clickYmas)
        self.ui.botonYmenos.clicked.connect(self.clickYmenos)

        #self.ui.reset_ceroButton.clicked.connect(self.resetZero)

        self.serial = serial.Serial('COM12', 115200)

         # Fill list with Baudrates 
        for baud in self.serial.BAUDRATES:
            self.ui.baudOptions.addItem(str(baud))

        # Set 115200 as default
        self.baud = 115200
        self.ui.baudOptions.setCurrentIndex(self.serial.BAUDRATES.index(self.baud))

         # Get available ports
        ports = list_ports.comports()
        
        # if any port exists, open port 
        if ports:
            for port in ports:
                self.ui.portOptions.addItem(port.device)

            self.serial.baudrate = self.baud
            #self.serial.port = self.ui.portOptions.currentText()
            self.ui.connectButton.setEnabled(True)

         # Create a Timer for reading data
        # self.readTimer = QtCore.QTimer()
        # self.readTimer.timeout.connect(self.read)
        
         # Connect signals - slots
        
        #self.ui.inputEdit.returnPressed.connect(self.send)
        # Current index changed -> self.changeBaud
        self.ui.baudOptions.currentIndexChanged.connect(self.changeBaud)
       # Clicked refresh button -> self.refresh
        self.ui.refreshButton.clicked.connect(self.refresh)
        # Clicked clear button -> self.clear
        self.ui.clearButton.clicked.connect(self.clear)
        # Clicked stop button -> self.stop
        self.ui.stopButton.clicked.connect(self.stop)

    def showCamera(self):
        self.camara = ViewImage()
        #self.camara.photo.connect()
    

    def clear(self):
         self.ui.textEdit.clear()

    
    def refresh(self):  
        # Get available ports
        ports = list_ports.comports()
        
        self.ui.portOptions.clear()
        # if any port exists, open port 
        if ports:
            for port in ports:
                self.ui.portOptions.addItem(port.device)

            self.serial.baudrate = self.baud
            self.serial.port = self.ui.portOptions.currentText()
            self.ui.connectButton.setEnabled(True)

    def changeBaud(self, index):
        self.baud = self.ui.baudOptions.itemText(index)
        if self.serial.is_open:
            self.serial.baudrate = self.baud
            self.serial.close()
            self.serial.open()

    def updateText(self, text):
        self.ui.textEdit.insertPlainText(text)
        self.ui.textEdit.moveCursor(QtGui.QTextCursor.End)


    def play(self):
        self.thread = QtCore.QThread()
        self.readPort = ReadPort(self.serial)
        self.readPort.moveToThread(self.thread)
        self.thread.started.connect(self.readPort.run)
        self.readPort.setFileName(self.fileName)
        self.thread.start()


    def stop(self):
        self.readPort.running=0
        self.thread.quit()
        
    def __del__(self):
        if self.serial.is_open:
            self.serial.close()

    
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
        self.openFileAndShow()


    def openFileAndShow(self):    
        
        self.__editor.setText(open(self.fileName).read().replace(";"," ")) 

        gcode= open(self.fileName).read().replace(";"," ") 
        self.view_3D.compute_data(gcode)
        self.view_3D.draw()       
      

    def openSVGFile(self):

        self.fileName = QFileDialog.getOpenFileName(self, "Open file", "/home/", 
                                                "*.svg *.gcode")[0]
        
        gcode_compiler = Compiler(interfaces.Gcode, movement_speed=1000, cutting_speed=300, pass_depth=5)
        curves = parse_file(self.fileName) # Parse an svg file into geometric curves
        gcode_compiler.append_curves(curves) 
        self.fileName = self.fileName.replace(".svg",".gcode")
        gcode_compiler.compile_to_file(self.fileName, passes=2)
     
        self.openFileAndShow()
        

class ViewImage(QWidget):
    photo = QtCore.pyqtSignal()


    def __init__(self):
        super().__init__()

        pygame.camera.init()
        cameras = pygame.camera.list_cameras()
        self.cam = pygame.camera.Camera(cameras[0],(320,240)) 

        self.label = QLabel()
        self.tomarfoto = QPushButton("Tomar foto")

        self.grid = QGridLayout()
        self.grid.addWidget(self.label)
        self.grid.addWidget(self.tomarfoto)
        self.setLayout(self.grid)

        self.timer = QTimer()
        self.timer.timeout.connect(self.showCamera)

        self.tomarfoto.clicked.connect(self.takephoto)

        self.cam.start()
        self.timer.start(33)

        self.show()
    
    def takephoto(self):

        #self.cap = cv2.VideoCapture("http://ip:port/video")    
        #self.timer.start(33)

        image = self.cam.get_image()
        raw_str = pygame.image.tostring(image, 'RGB', False)
        pil_image = Image.frombytes('RGB', image.get_size(), raw_str)
        
        self.im = ImageQt.ImageQt(pil_image)
        pixmap = QPixmap.fromImage(self.im)
        self.label.setPixmap(pixmap)
        pixmap.save("photo0.bmp")
        
        input_file = "photo0.bmp"
        output_file = "photo.svg" 
        os.system("potrace {} --svg -o {}".format(input_file, output_file))

        #svg = cairosvg.svg2svg(
        #url='photo.svg', 
        #write_to='photo.svg', 
        #scale=0.5
        #   )  

    def __del__(self):
        self.cam.stop()

    #def stopCamera(self):    
        #self.timer.stop()

    def showCamera(self):
        image = self.cam.get_image()
        raw_str = pygame.image.tostring(image, 'RGB', False)
        pil_image = Image.frombytes('RGB', image.get_size(), raw_str)
        

        self.im = ImageQt.ImageQt(pil_image)
        pixmap = QPixmap.fromImage(self.im)
        self.label.setPixmap(pixmap)


if __name__ == "__main__": 
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()


