import socket
import sys
import tqdm


def send_packet(conn, packet, progress=False, filename=None):
    size = (len(packet)).to_bytes(4, 'big')
    print(len(packet))
    if progress:
        BUFFER_SIZE = 1024*4
        bar = tqdm.tqdm(range(len(packet)), f"Sending{filename}", unit="B", unit_scale=True, unit_divisor=1024)
        i = 0
        conn.sendall(size)
        for _ in bar:
            part = packet[i : i + BUFFER_SIZE]
            i += BUFFER_SIZE
            conn.sendall(part)
            bar.update(i)
        return
    packet = size + packet
    conn.sendall(packet)


def get_bytes_from_file(filename):
    return open(filename, "rb").read()


args = sys.argv
IP = args[2]
PORT = int(args[3])

clientSock = socket.socket()
clientSock.connect((IP, PORT))
name = args[1]
file = get_bytes_from_file(name)
send_packet(clientSock, name.encode('utf-8'))
send_packet(clientSock, file, True, filename=name)