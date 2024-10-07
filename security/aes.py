from Crypto.Cipher import AES

from security.dh import DHSecurity


class AESecurity:
    def __init__(self, peer_public_key):
        # self._dh = DHSecurity() [deprecated]
        # self._secret_key = bytes(self._dh.shared_secret(peer_public_key))
        self._secret_key = b"#7i$Gq9yxlR7JN@$UT8M$SjfEY8GxgvoHAcE5Umts2W^g$j79fE*69bnLFds"

    def encrypt(self, text: str):
        cipher = AES.new(self._secret_key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(text.encode('utf-8'))
        return ciphertext, tag, cipher.nonce

    def decrypt(self, ciphertext, tag, nonce):
        try:
            # will raise exception if the message has been tempered with
            cipher = AES.new(self._secret_key, AES.MODE_EAX, nonce=nonce)
            bytes_text = cipher.decrypt_and_verify(ciphertext, tag)
            return bytes_text.decode('utf-8')
        except Exception as e:
            raise Exception(str(e))
