import socket
from os import listdir


def receive_packet(connection):
    size = None
    while size is None:
        size = connection.recv(4)
    size = int.from_bytes(size, 'big')
    d = b''
    while len(d) != size:
        part = None
        while part is None:
            part = connection.recv(size - len(d))
        d += part
    print(len(d))
    return d


servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servSock.bind(('localhost', 5001))
servSock.listen(1)

conn, addr = servSock.accept()
name = receive_packet(conn).decode('utf-8')
pr_name = name.split('.')
file = receive_packet(conn)
i = 1
while name in listdir('.'):
    name = pr_name[0] + f'_copy{i}.' + pr_name[1]
    i += 1
fd = open(name, 'wb')
fd.write(file)
fd.close()
print(f'received {name}')
