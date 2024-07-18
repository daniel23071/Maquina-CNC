from doctest import OutputChecker
import sys

import pygame.camera
from PIL import Image, ImageQt

from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QGridLayout,
    QWidget
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer


class ViewImage(QWidget):
        def __init__(self):
            super().__init__()

            pygame.camera.init()
            cameras = pygame.camera.list_cameras()
            self.cam = pygame.camera.Camera(cameras[0])
            self.label = QLabel()

            self.grid = QGridLayout()
            self.grid.addWidget(self.label)
            self.setLayout(self.grid)

            self.timer = QTimer()
            self.timer.timeout.connect(self.showCamera)
            self.cam.start()
            self.timer.start(33)

            self.show()


        def showCamera(self):
            image = self.cam.get_image()
            raw_str = pygame.image.tostring(image, 'RGB', False)
            pil_image = Image.frombytes('RGB', image.get_size(), raw_str)

            self.im = ImageQt.ImageQt
            pixmap = QPixmap.fromImage(self.im)

            self.label.setPixmap(pixmap)

if __name__== "__main__":
        app = QApplication(sys.argv)
        view = ViewImage()
        sys.exit(app.exec())                


#
#input_file = "photo.bmp"
#Output_file = "photo.svg"

#os.system("potrace {} --svg -o {}".format(input_file, Output_file))