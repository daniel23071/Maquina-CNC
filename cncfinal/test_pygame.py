from turtle import delay
import pygame
import pygame.camera

from PIL import Image, ImageFilter
from time import sleep


pygame.init()
pygame.camera.init() 

cameras = pygame.camera.list_cameras()

print(cameras)
cam = pygame.camera.Camera(cameras[0], (640, 480))

cam.start()
sleep(2)

image = cam.get_image()
#print(image)
cam.stop()

raw_str = pygame.image.tostring(image, 'RGB')
pil_image = Image.frombytes('RGB', image.get_size(), raw_str)

pil_image = pil_image.convert('L')

threshold = 100
img_new = pil_image.point(lambda x:255 if x > threshold else 0)
img_new.show()
img_new = img_new.filter(ImageFilter.CONTOUR)

img_new.show()
img_new.save('photo.mbp')