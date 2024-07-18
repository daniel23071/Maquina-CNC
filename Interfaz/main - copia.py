from PyQt5 import QtWidgets, uic
import sys
import serial


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        self.ui = uic.loadUi('INTERFAZCNC.ui', self)
        self.ui.botonZmas.clicked.connect(self.clickZmas)
        self.serial = serial.Serial('COM10', 115200)

                
    def clickZmas(self):
        dataZ0="$G\n"
        dataZ1="$J=G21G91X0Y0Z1F10\n"
        self.serial.write(dataZ0.encode('utf-8'))
        self.serial.write(dataZ1.encode('utf-8'))
    
        """
        self.serial.write("$0=10\n")
        self.serial.write("$1=25\n")
        self.serial.write("$2=0\n")
        self.serial.write("$3=0\n")
        self.serial.write("$4=0\n")
        self.serial.write("$5=0\n")
        self.serial.write("$6=0\n")
        self.serial.write("$10=1\n")
        self.serial.write("$11=0.010\n")
        self.serial.write("$12=0.002\n")
        self.serial.write("$13=0\n")
        self.serial.write("$20=0\n")
        self.serial.write("$21=0\n")
        self.serial.write("$22=0\n")
        self.serial.write("$23=0\n")
        self.serial.write("$24=25.000\n")
        self.serial.write("$25=500.000\n")
        self.serial.write("$26=250\n")
        self.serial.write("$27=1.000\n")
        self.serial.write("$30=1000\n")
        self.serial.write("$31=0\n")
        self.serial.write("$32=0\n")
        self.serial.write("$100=250.000\n")
        self.serial.write("$101=250.000\n")
        self.serial.write("$102=250.000\n")
        self.serial.write("$110=500.000\n")
        self.serial.write("$111=500.000\n")
        self.serial.write("$112=500.000\n")
        self.serial.write("$120=10.000\n")
        self.serial.write("$121=10.000\n")
        self.serial.write("$122=10.000\n")
        self.serial.write("$130=200.000\n")
        self.serial.write("$131=200.000\n")
        self.serial.write("$132=200.000\n")
        """

 

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()