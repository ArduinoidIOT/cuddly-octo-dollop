import socket
import curve25519
import os
from Crypto.Cipher import ChaCha20_Poly1305
from base64 import b64decode, b64encode

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
            prv = curve25519.generatePrivateKey(os.urandom(32))
            pub = curve25519.generatePublicKey(prv)
            conn.send(pub)
            conn.send(b'\n')
            data = getdata(33, conn).strip()
            if data == b'':
                break
            key = curve25519.calculateAgreement(prv, data)
            nonce = os.urandom(12)
            conn.send(nonce)
            while True:
                cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
                ciphertext = receiveuntil(b'\n', conn)
                sig = getdata(25, conn).strip()
                data = cipher.decrypt_and_verify(b64decode(ciphertext), b64decode(sig))
                print(data.decode())
                if data == b'exit':
                    break
                cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
                with open(data.decode(), 'rb') as file:
                    ctxt, sig = cipher.encrypt_and_digest(file.read())
                    # data = file.read()
                conn.send(b64encode(ctxt))
                conn.send(b'\n')
                conn.send(b64encode(sig))
                conn.send(b'\n')
