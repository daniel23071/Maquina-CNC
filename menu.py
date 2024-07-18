# Modules PyQt
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *
import serial
import serial.tools.list_ports as list_ports
import time
import sys
import view3d


# Class Monitor - Inherits from QMainWindow
class Menu(QtWidgets.QMainWindow):

    # Constructor
    def __init__(self):
        super(Menu, self).__init__()
        # Load user interface
        self.ui = uic.loadUi("INTERFAZ_GRUPO.ui", self)
        
        # Serial port object 
        self.serial = serial.Serial()
        self.fileName = ''
        self.comandos = ''
        #Visualiza Gcode en 3D
        self.view_3D = view3d.View3D()
        self.ui.viewLayout.addWidget(self.view_3D)

        #Visualiza texto de comandos
        self.__editor = QsciScintilla()
        self.ui.codeLayout.addWidget(self.__editor)
        
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(12)
        
        lexer = QsciLexerPython()
        lexer.setDefaultFont(font)
        self.__editor.setLexer(lexer)
        self.__editor.setUtf8(True)  # Set encoding to UTF-8
        self.__editor.setFont(font) 
        self.__editor.setMarginsFont(font) 
        
        fontmetrics = QFontMetrics(font)
        self.__editor.setMarginsFont(font)
        self.__editor.setMarginWidth(0, fontmetrics.width("0000") + 6)
        self.__editor.setMarginLineNumbers(0, True)
        self.__editor.setMarginsBackgroundColor(QColor("#cccccc"))

        for baud in self.serial.BAUDRATES:
            self.ui.baudOptions.addItem(str(baud))

        self.baud = 115200
        self.ui.baudOptions.setCurrentIndex(self.serial.BAUDRATES.index(self.baud))

        ports = list_ports.comports()
        
        if ports:
            for port in ports:
                self.ui.portOptions.addItem(port.device)

            self.serial.baudrate = self.baud
            self.serial.port = self.ui.portOptions.currentText()
            self.ui.connectButton.setEnabled(True)

        self.readTimer = QtCore.QTimer()

        self.readTimer.timeout.connect(self.read)
        self.ui.connectButton.clicked.connect(self.connect)
        self.ui.X_izquierda.clicked.connect(self.X_L)
        self.ui.inputEdit.returnPressed.connect(self.send)
        self.ui.baudOptions.currentIndexChanged.connect(self.changeBaud)
        self.ui.X_derecha.clicked.connect(self.X_R)
        self.ui.Y_arriba.clicked.connect(self.Y_UP)
        self.ui.Y_abajo.clicked.connect(self.Y_DOWN)
        self.ui.Diag_Der_UP.clicked.connect(self.R_DiagUP)
        self.ui.Diag_Izq_UP.clicked.connect(self.L_DiagUP)
        self.ui.Diag_Der_DOWN.clicked.connect(self.R_DiagDOWN)
        self.ui.Diag_Izq_DOWN.clicked.connect(self.L_DiagDOWN)
        self.ui.openButton.clicked.connect(self.abrir_archivo)
        self.ui.iniciarButton.clicked.connect(self.ejecutar)
        self.ui.reset_ceroButton.clicked.connect(self.resetZero)
        self.ui.ceroButton.clicked.connect(self.returnZero)
        self.pararButton.clicked.connect(self.stop)
               
        self.timer = QtCore.QTimer()
        if self.serial.is_open:
            self.timer.start(10)
            self.timer.timeout.connect(self.read)

    def clear(self):
        self.ui.textEdit.clear()
	
    def connect(self):
        if not self.serial.is_open:
            self.serial.open()       
            self.readTimer.start(10)
            self.ui.sendButton.setEnabled(True)
            self.ui.connectButton.setText('Disconnect')
            self.ui.inputEdit.setEnabled(True)
        else:
            self.serial.close()
            self.readTimer.stop()
            self.ui.sendButton.setEnabled(False)
            self.ui.connectButton.setText('Connect')
            self.ui.inputEdit.setEnabled(False)

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

    def read(self):
        if self.serial.is_open:
            if self.serial.in_waiting > 0:
                data = self.serial.read()
                data = data.replace(b'\r', b'')
                text = data.decode('iso-8859-1')
                self.ui.textEdit.insertPlainText(text)
                self.ui.textEdit.moveCursor(QtGui.QTextCursor.End)

    def abrir_archivo(self):
        self.fileName = QFileDialog.getOpenFileName(self, "Open file", "/home/alejandro", 
                                                "*.gcode *.ngc")[0]
        self.ui.textEdit.setText(self.fileName)
        self.visual3D()

    def visual3D(self):
        gcode = open(self.fileName).read()
        self.view_3D.compute_data(gcode)
        self.view_3D.draw()

    def ejecutar(self):
        f = open(self.fileName, 'r')
        time.sleep(2)
        self.send_message("\n\n")
        for line in f:
            comando = line.strip()
            if not comando.startswith('(') and not comando.startswith('%'):
                self.send_message(comando)
                self.__editor.append(comando + '\n')
                self.comandos += '\n' + comando + '\n'
                self.ui.textEdit.setText('algo')
                
        f.close()

    def resetZero(self):
        self.send_message('G10 P0 L20 X0 Y0 Z0')

    def returnZero(self):
        self.send_message('G21G90 G0Z5')
        self.send_message('G90 G0 X0 Y0')
        self.send_message('G90 G0 Z0')

    def stop(self):
        self.send_message('GC:G0 G54 G17 G21 G90 G94 M5 M9 T0 F0')

    def Y_UP(self):
        self.send_message('G21G91G1Y1F10')
        self.send_message('G90G21')

    def Y_DOWN(self):
        self.send_message('G21G91G1Y-1F10')
        self.send_message('G90G21')

    def X_L(self):
        self.send_message('G21G91G1X-1F10')
        self.send_message('G90G21')

    def X_R(self):
        self.send_message('G21G91G1X1F10')
        self.send_message('G90G21')

    def R_DiagDOWN(self):
        self.send_message('G21G91X1Y-1F10')
        self.send_message('G90G21')

    def R_DiagUP(self):
        self.send_message('G21G91X1Y1F10')
        self.send_message('G90G21')

    def L_DiagUP(self):
        self.send_message('G21G91X-1Y1F10')
        self.send_message('G90G21')

    def L_DiagDOWN(self):
        self.send_message('G21G91X-1Y-1F10')
        self.send_message('G90G21')

    def send_message(self, message):
        text = self.ui.textEdit.toPlainText()
        text += message + '\n'
        self.ui.textEdit.setText(text)
        data = message + '\n'
        self.serial.write(data.encode('utf-8'))
        lectura = self.serial.readline().decode('utf-8')



    def send(self):
        if self.serial.is_open:
            data = self.ui.inputEdit.text() + '\n'
            self.serial.write(data.encode('iso-8859-1'))
            self.ui.inputEdit.setText('')


    def __del__(self):
        if self.serial.is_open:
            self.serial.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    menu = Menu()
    menu.show()
    app.exec_()