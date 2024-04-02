from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes

# Generate RSA key pair
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    # Serialize private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem

# Encrypt a string using RSA public key
def encrypt_string(message, public_key):
    public_key = public_key.encode() #since the dictionary stores a decoded version of the public key
    public_key_obj = serialization.load_pem_public_key(public_key)
    ciphertext = public_key_obj.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

# Decrypt RSA encrypted data using private key
def decrypt_string(ciphertext, private_key):
    private_key_obj = serialization.load_pem_private_key(
        private_key,
        password=None
    )
    plaintext = private_key_obj.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()

# Example usage
# private_key, public_key = generate_rsa_key_pair()

# # Encrypt a message
# message = "Hello, world!"
# encrypted_data = encrypt_string(message, public_key.decode())
# print("Encrypted:", encrypted_data)

# # Decrypt the encrypted data
# decrypted_message = decrypt_string(encrypted_data, private_key)
# print("Decrypted:", decrypted_message)
