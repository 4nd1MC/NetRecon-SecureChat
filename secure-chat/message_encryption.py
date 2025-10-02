from __future__ import annotations
import os, base64
from typing import Tuple
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class MessageEncryption:
    def __init__(self, passphrase: str, salt: bytes | None = None):
        self.passphrase = passphrase
        self.salt = salt or os.urandom(16)
        self.key = self._derive(self.passphrase, self.salt)

    @staticmethod
    def _derive(passphrase: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=200_000,
        )
        return kdf.derive(passphrase.encode())

    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> bytes:
        aes = AESGCM(self.key)
        nonce = os.urandom(12)
        ct = aes.encrypt(nonce, plaintext, aad)
        return b"|".join([self.salt, nonce, ct])

    def decrypt(self, blob: bytes, aad: bytes = b"") -> bytes:
        salt, nonce, ct = blob.split(b"|", 2)
        key = self._derive(self.passphrase, salt)
        aes = AESGCM(key)
        return aes.decrypt(nonce, ct, aad)

def pack_str(s: str) -> bytes:
    return s.encode()

def unpack_str(b: bytes) -> str:
    return b.decode()

def encode64(b: bytes) -> str:
    return base64.b64encode(b).decode()

def decode64(s: str) -> bytes:
    return base64.b64decode(s.encode())