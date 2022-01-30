import socket
import threading

sock = socket.socket()

sock.bind(('localhost', 8088))

sock.listen()

conns = list()

def send(conn):
    global conns
    while True:
        data = conn.recv(100)
        for connection in conns:
            if not(connection == conn):
                connection.send(data)


while True:
    conn, addr = sock.accept()
    conns.append(conn)
    t = threading.Thread(target=send, args=(conn,), daemon=True)
    t.start()