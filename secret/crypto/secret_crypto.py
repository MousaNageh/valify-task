import os

from cryptography.fernet import Fernet


class SecretCrypto:
    _fernet = Fernet(os.environ.get("SECRET_CRYPTO_KEY"))

    @classmethod
    def encrypt_secret(cls, secret: str):
        encrypted = cls._fernet.encrypt(secret.encode())
        return encrypted.decode()

    @classmethod
    def decrypt_secret(cls, encrypted_secret: str):
        decrypted = cls._fernet.decrypt(encrypted_secret)
        return decrypted.decode()
