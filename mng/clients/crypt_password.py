from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key

with open("databases/encrypt/keys/clients_password/public_key.pem", "rb") as public_key_file:
    public_key = load_pem_public_key(public_key_file.read())

with open("databases/encrypt/keys/clients_password/private_key.pem", "rb") as private_key_file:
    private_key = load_pem_private_key(private_key_file.read(), password=None)

def encrypt_password(password):
    """Encrypt the password using the public RSA key."""
    encrypted_password = public_key.encrypt(
        password.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_password

def decrypt_password(encrypted_password):
    """Decrypt the password using the private RSA key."""
    decrypted_password = private_key.decrypt(
        encrypted_password,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_password.decode('utf-8')
