from PyQt5 import QtWidgets, uic
import sys
import serial


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        self.ui = uic.loadUi('INTERFAZCNC.ui', self)

        self.ui.botonZmas.clicked.connect(self.clickZmas)
        self.ui.botonZmenos.clicked.connect(self.clickZmenos)

        self.ui.botonXmas.clicked.connect(self.clickXmas)
        self.ui.botonXmenos.clicked.connect(self.clickXmenos)

        self.ui.botonYmas.clicked.connect(self.clickYmas)
        self.ui.botonYmenos.clicked.connect(self.clickYmenos)

        self.serial = serial.Serial('COM10', 115200)

                
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
 

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()