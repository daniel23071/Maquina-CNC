import serial
import time

s = serial.Serial('/dev/ttyUSB0', 115200)

f = open('INTERFAZCNC.ui', 'r')

s.write("\n\n".encode('utf-8'))
time.sleep(2)
s.flushInput()

for line in f:
    l = line.strip()
    if not l.startswith('(') and not l.startswith('%'):
        print('Sending: '+ l)
        s.write((l + '\n').encode('utf-8'))
        grbl_out = s.readline().decode('utf-8')
        print(': '+grbl_out.strip())


input("  Press <Enter> to exit and disable grbl.") 

f.close()
s.close()
