import os
import sys
import argparse
import shutil
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets

DEFAULT_PASSWORD = "random12345"

def has_write_permission(directory):
    """Check if the directory is writable."""
    return os.access(directory, os.W_OK)

def get_files_from_directory(directory):
    """Return a list of file paths from the given directory."""
    files = []
    for entry in os.scandir(directory):
        if entry.is_file():
            files.append(entry.path)
    return files

def encrypt_file(
    file_path,
    password=DEFAULT_PASSWORD,
    delete_original=False,
    move_to_folder=None
):
    """
    Encrypts a file using AES-GCM with a key derived from the password using PBKDF2.
    Optionally deletes the original and/or moves the encrypted file.
    Returns the path to the encrypted file, or None on failure.
    """
    try:
        salt = secrets.token_bytes(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(password.encode('utf-8'))
        nonce = secrets.token_bytes(12)
        cipher = AESGCM(key)
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted_data = cipher.encrypt(nonce, data, None)
        complete_package = salt + nonce + encrypted_data
        file_name, file_extension = os.path.splitext(file_path)
        if file_extension.startswith('.'):
            file_extension = file_extension[1:]
        encrypted_file_path = f"{file_name}.{file_extension}.encrypted"
        with open(encrypted_file_path, 'wb') as f:
            f.write(complete_package)

        # Move encrypted file if requested
        if move_to_folder:
            os.makedirs(move_to_folder, exist_ok=True)
            dest_path = os.path.join(move_to_folder, os.path.basename(encrypted_file_path))
            shutil.move(encrypted_file_path, dest_path)
            encrypted_file_path = dest_path

        # Delete original if requested
        if delete_original:
            try:
                os.remove(file_path)
                print(f"Deleted original: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

        return encrypted_file_path
    except Exception as e:
        print(f"Error encrypting file: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Encrypt a file or all files in a directory.')
    parser.add_argument('file', nargs='?', help='File to encrypt')
    parser.add_argument('--dir', help='Encrypt all files in this directory')
    parser.add_argument('--password', default=DEFAULT_PASSWORD, help='Password for encryption')
    parser.add_argument('--delete-original', action='store_true', help='Delete original file(s) after encryption')
    parser.add_argument('--move-to', help='Move encrypted file(s) to this folder')
    args = parser.parse_args()

    files_to_encrypt = []

    if args.dir:
        if not os.path.isdir(args.dir):
            print(f"Error: Directory '{args.dir}' not found")
            sys.exit(1)
        if not has_write_permission(args.dir):
            print(f"Error: No write permission for directory '{args.dir}'")
            sys.exit(1)
        files_to_encrypt = get_files_from_directory(args.dir)
        if not files_to_encrypt:
            print(f"No files found in directory '{args.dir}'")
            sys.exit(0)
    elif args.file:
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found")
            sys.exit(1)
        files_to_encrypt = [args.file]
    else:
        print("Error: Please specify a file or directory to encrypt.")
        sys.exit(1)

    for file_path in files_to_encrypt:
        result_file = encrypt_file(
            file_path,
            password=args.password,
            delete_original=args.delete_original,
            move_to_folder=args.move_to
        )
        if result_file:
            print(f"File encrypted successfully: {result_file}")
        else:
            print(f"Encryption failed for: {file_path}")

if __name__ == "__main__":
    main()
