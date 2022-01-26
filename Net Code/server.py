import socket
import threading

sock = socket.socket()

sock.bind(('localhost', 8088))

sock.listen()

conn, addr = sock.accept()

while True:
    data = conn.recv(1000)
    if data:
        print(data.decode("UTF-8"))