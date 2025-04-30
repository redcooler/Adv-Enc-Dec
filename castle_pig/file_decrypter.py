import os
import sys
import argparse
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

DEFAULT_PASSWORD = "random12345"

def decrypt_file(file_path, password=DEFAULT_PASSWORD):
    """
    Decrypts a file that was encrypted with encrypt_file.
    Returns the path to the decrypted file, or None on failure.
    """
    try:
        with open(file_path, 'rb') as f:
            complete_package = f.read()
        salt = complete_package[:16]
        nonce = complete_package[16:28]
        encrypted_data = complete_package[28:]
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(password.encode('utf-8'))
        cipher = AESGCM(key)
        try:
            decrypted_data = cipher.decrypt(nonce, encrypted_data, None)
        except Exception as e:
            print(f"Decryption failed. Incorrect password or corrupted file: {e}")
            return None
        if file_path.endswith('.encrypted'):
            decrypted_file_path = file_path[:-10]
        else:
            decrypted_file_path = file_path + '.decrypted'
        with open(decrypted_file_path, 'wb') as f:
            f.write(decrypted_data)
        return decrypted_file_path
    except Exception as e:
        print(f"Error decrypting file: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Decrypt a file')
    parser.add_argument('file', help='File to decrypt')
    parser.add_argument('--password', default=DEFAULT_PASSWORD, help='Password for decryption')
    args = parser.parse_args()
    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)
    result_file = decrypt_file(args.file, args.password)
    if result_file:
        print(f"File decrypted successfully: {result_file}")
    else:
        print("Decryption failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
