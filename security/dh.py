from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from util.endpoints import Endpoints

######################################################################################################
#                                      **Deprecated**                                                #
#                                                                                                    #
#             (Incompatibility with existing Pico libraries the DHH ECC had to be removed.)          #
######################################################################################################


def generate_keys():
    endpoints = Endpoints()
    try:
        private = ECC.generate(curve='p256')
        public = private.public_key()
        with open(endpoints.PRIVATE_KEY_PATH, "wt") as file:
            file.write(private.export_key(format='PEM'))
        with open(endpoints.PUBLIC_KEY_PATH, "wt") as file:
            file.write(public.export_key(format='PEM'))
        return True
    except Exception as e:
        raise Exception(str(e))


def get_public_key():
    endpoints = Endpoints()
    try:
        with open(endpoints.PUBLIC_KEY_PATH) as file:
            data = file.read()
            return ECC.import_key(data)
    except Exception as e:
        raise Exception(str(e))


class DHSecurity:
    def __init__(self):
        self._endpoints = Endpoints()
        self._private_key = self._read_private_key()
        self._shared_secret_cache = None

    def _read_private_key(self):
        try:
            with open(self._endpoints.PRIVATE_KEY_PATH, "r") as file:
                data = file.read()
                return ECC.import_key(data)
        except Exception as e:
            raise Exception(str(e))

    def shared_secret(self, peer_public_key):
        if self._shared_secret_cache:
            return self._shared_secret_cache

        if isinstance(peer_public_key, str):
            peer_public_key_local = ECC.import_key(peer_public_key)
        else:
            peer_public_key_local = peer_public_key

        shared_secret = peer_public_key_local.pointQ * self._private_key.d
        shared_bytes = shared_secret.x.to_bytes()
        secret_hash = SHA256.new(shared_bytes).digest()
        self._shared_secret_cache = secret_hash
        return secret_hash

