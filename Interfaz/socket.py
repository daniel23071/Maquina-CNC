import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('localhost', 65432))
s.listen()

while True:
    try:
        client, address = s.accept()
        print('Client connected')
        client.send(data)
    except KeyboardInterrupt:
        break
print('End server')


import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('localhost',  65432))
s.send(b'Hello')
data = s.recv(1024)

print(data)