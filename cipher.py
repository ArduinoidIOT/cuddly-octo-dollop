from hashlib import sha3_256


class Cipher:
    def __init__(self, encryption_key):

        self.key = encryption_key
        self.HMAC_encrypt = sha3_256()
        self.HMAC_decrypt = sha3_256()

    def encrypt(self, text):
        key_rep, key_part = divmod(len(text), 32)
        try:
            text = text.encode()
        except AttributeError:
            pass
        key = self.key * key_rep + self.key[: key_part]
        out = b''
        for a, b in zip(text, key):
            out += bytes([(a + b) % 255])
        self.HMAC_encrypt.update(out)
        return out

    def digest(self):
        return self.HMAC_encrypt.digest()

    def hex_digest(self):
        return self.HMAC_encrypt.hexdigest()

    def encrypt_and_digest(self, text):
        return self.encrypt(text), self.digest()

    def decrypt(self, cipher_text):
        self.HMAC_decrypt.update(cipher_text)
        key_rep, key_part = divmod(len(cipher_text), 32)
        try:
            cipher_text = cipher_text.encode()
        except AttributeError:
            pass
        key = self.key * key_rep + self.key[: key_part]
        out = b''
        for a, b in zip(cipher_text, key):
            out += bytes([(a - b) % 255])
        return out

    def verify(self, signature):
        assert signature == self.HMAC_decrypt.digest() or signature == self.HMAC_decrypt.hexdigest()
        return True

    def decrypt_and_verify(self, cipher_text, signature):
        return self.decrypt(cipher_text), self.verify(signature)
