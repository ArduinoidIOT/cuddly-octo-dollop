#!/usr/bin/python3
import socket
from base64 import b64decode

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


HOST = '127.0.0.1'
PORT = 65532
if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            cmd = input("$")
            s.send(cmd.encode() + b'\n')
            ciphertext = receiveuntil(b'\n', s)
            print(b64decode(ciphertext).decode())
