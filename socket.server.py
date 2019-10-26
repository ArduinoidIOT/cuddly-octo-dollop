import os
import socket
from base64 import b64encode

PORT = 65532


def getdata(byt, sock):
    targ = b''
    for _ in range(byt):
        targ += sock.recv(1)
    return targ


def receiveuntil(terminator, sock):
    char = sock.recv(1)
    ret = b''
    while char != terminator:
        ret += char
        char = sock.recv(1)
    return ret


def process(instruction):
    ins = instruction.split(' ')
    if ins[0] == 'mkdir':
        try:
            mode = int('0o' + ins[ins.index('--mode') + 1])
            os.mkdir(ins[1], mode)
        except OSError:
            os.mkdir(ins[1])


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        print(addr)
        with conn:
            while True:
                data = receiveuntil(b'\n', conn)
                if data == b'exit':
                    break
                print(data.decode())
                with open(data.decode(), 'rb') as file:
                    data = file.read()
                conn.send(b64encode(data) + b'\n')
