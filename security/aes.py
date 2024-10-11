from Crypto.Cipher import AES
import hashlib
from util.program_codes import AesMode


class AESecurity:
    def __init__(self, mode: AesMode):
        hashing = hashlib.sha256()
        match mode:
            case AesMode.USER:
                hashing.update(b"&dNKNE3*jkEKPmHNK@5hi5fH7uDgK2g$")
                self._secret_key = hashing.digest()
            case AesMode.PICO:
                hashing.update(b"5r*7t^Ed4&zniGC9!jyy7np@PS%px737")
                self._secret_key = hashing.digest()
            case _:
                self._secret_key = None

    def encrypt(self, data: bytes):
        try:
            if not self._secret_key:
                raise Exception("Could not encrypt the secret key is None.")
            cipher = AES.new(self._secret_key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(data)
            return ciphertext, tag, cipher.nonce
        except Exception as e:
            raise Exception(str(e))

    def decrypt(self, ciphertext, tag, nonce):
        try:
            if not self._secret_key:
                raise Exception("Could not decrypt the secret key is None.")
            # will raise exception if the message has been tempered with
            cipher = AES.new(self._secret_key, AES.MODE_EAX, nonce=nonce)
            decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
            return decrypted_data
        except Exception as e:
            raise Exception(str(e))
