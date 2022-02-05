import socket
import threading

sock = socket.socket()

sock.bind(('localhost', 8088))

sock.listen(2)

conns = list()

def send(conn):
    global conns

    if len(conns) == 1:
        while len(conns) != 2:
            pass
        conn.send(bytes("Connected", encoding="UTF-8"))
        conn.send(bytes("0", encoding="UTF-8"))
    elif len(conns) == 2:
        conn.send(bytes("Connected", encoding="UTF-8"))
        conn.send(bytes("1", encoding="UTF-8"))
        
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