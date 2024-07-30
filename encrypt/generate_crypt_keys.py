from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

def generate_rsa_key_pair(directory, private_key_filename="private_key.pem", public_key_filename="public_key.pem"):
    # ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # save the private key to a file
    private_key_path = os.path.join(directory, private_key_filename)
    with open(private_key_path, "wb") as private_key_file:
        private_key_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # save the public key to a file
    public_key = private_key.public_key()
    public_key_path = os.path.join(directory, public_key_filename)
    with open(public_key_path, "wb") as public_key_file:
        public_key_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    print(f"RSA key pair generated and saved in {directory}.")

if __name__ == "__main__":
    generate_rsa_key_pair("databases/encrypt/keys/clients_password")
    generate_rsa_key_pair("databases/encrypt/keys/wallets_keys")
