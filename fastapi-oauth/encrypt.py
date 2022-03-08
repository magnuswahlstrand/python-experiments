import base64
import json
import rsa

with open('private-key.pem', mode='rb') as f:
    privdata = f.read()
privkey = rsa.PrivateKey.load_pkcs1(privdata)

with open('public-key.pem', mode='rb') as f:
    pubdata = f.read()
pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(pubdata)


def encrypt_message(message: str):
    encrypted = rsa.encrypt(json.dumps(message).encode(), privkey)
    encrypted_b64 = base64.b64encode(encrypted).decode()
    return encrypted_b64


def decrypt_message(encrypted_b64: str):
    encrypted = base64.b64decode(encrypted_b64.encode())
    decrypted = rsa.decrypt(encrypted, privkey)
    return json.loads(decrypted)
