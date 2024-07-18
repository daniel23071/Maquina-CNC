from time import sleep
import pygame
import sys
import pygame.camera
from PIL import Image, ImageQt
from PIL import Image

pygame.init()
pygame.camera.init()

cameras= pygame.camera.list_cameras()
print(cameras)

cam = pygame.camera.Camera(cameras[0], (640, 480))
cam.start() 

image= cam.get_image()
print(image)

raw_str = pygame.image.tostring(image, 'RGB')
pil_image = Image.frombytes('RGB', image.get_size(), raw_str)
pil_image.show()