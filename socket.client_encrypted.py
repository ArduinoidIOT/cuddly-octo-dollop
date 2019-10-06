import socket
import curve25519
import os
from Crypto.Cipher import ChaCha20_Poly1305
from base64 import b64encode, b64decode


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


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65532  # The port used by the server
if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        prv = curve25519.generatePrivateKey(os.urandom(32))
        pub = curve25519.generatePublicKey(prv)
        data = getdata(33, s).strip()
        if not data:
            exit()
        s.send(pub)
        s.send(b'\n')
        key = curve25519.calculateAgreement(prv, data)
        nonce = getdata(12, s)
        while True:
            cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
            cmd = input("$")
            ctxt, sig = cipher.encrypt_and_digest(cmd.encode())
            s.send(b64encode(ctxt))
            #s.send(b64encode(cmd.encode()))
            s.send(b'\n')
            s.send(b64encode(sig))
            s.send(b'\n')
            cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
            ciphertext = receiveuntil(b'\n', s)
            sig = getdata(25, s).strip()
            data = cipher.decrypt_and_verify(b64decode(ciphertext), b64decode(sig))
            print(data.decode())