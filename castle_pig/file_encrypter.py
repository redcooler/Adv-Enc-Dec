# file_encrypter.py

import os
import sys
import argparse
import shutil
import secrets
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Import the secure_delete module from your package
try:
    import castle_pig.secure_delete as secure_delete
except ImportError:
    # Fallback for standalone use or testing
    import secure_delete

DEFAULT_PASSWORD = "random12345"

def has_write_permission(directory):
    """Check if the directory is writable."""
    return os.access(directory, os.W_OK)

def get_files_from_directory(directory):
    """Return a list of file paths from the given directory."""
    files = []
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found", file=sys.stderr)
        return []
    if not has_write_permission(directory):
        print(f"Error: No write permission for directory '{directory}'", file=sys.stderr)
        return []
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
    Optionally deletes the original securely using secure_delete module
    and/or moves the encrypted file.
    Returns the path to the encrypted file, or None on failure.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found", file=sys.stderr)
        return None

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
            try:
                os.makedirs(move_to_folder, exist_ok=True)
                dest_path = os.path.join(move_to_folder, os.path.basename(encrypted_file_path))
                shutil.move(encrypted_file_path, dest_path)
                encrypted_file_path = dest_path
                print(f"Moved encrypted file to: {encrypted_file_path}")
            except Exception as e:
                print(f"Error moving encrypted file: {e}", file=sys.stderr)

        # Delete original securely if requested
        if delete_original:
            secure_delete.secure_delete(file_path)

        return encrypted_file_path
    except Exception as e:
        print(f"Error encrypting file: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description='Encrypt a file or all files in a directory.')
    parser.add_argument('file', nargs='?', help='File to encrypt')
    parser.add_argument('--dir', help='Encrypt all files in this directory')
    parser.add_argument('--password', default=DEFAULT_PASSWORD, help='Password for encryption')
    parser.add_argument('--delete-original', action='store_true', help='Delete original file(s) after encryption (securely, if possible)')
    parser.add_argument('--move-to', help='Move encrypted file(s) to this folder')
    args = parser.parse_args()

    files_to_process = []

    if args.dir:
        files_to_process = get_files_from_directory(args.dir)
        if not files_to_process:
            print(f"No files found in directory '{args.dir}' to encrypt.")
            sys.exit(0)
    elif args.file:
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)
        files_to_process = [args.file]
    else:
        print("Error: Please specify a file or directory to encrypt.", file=sys.stderr)
        sys.exit(1)

    encryption_password = args.password if args.password else DEFAULT_PASSWORD

    for file_path in files_to_process:
        result_file = encrypt_file(
            file_path,
            password=encryption_password,
            delete_original=args.delete_original,
            move_to_folder=args.move_to
        )
        if result_file:
            print(f"File encrypted successfully: {result_file}")
        else:
            print(f"Encryption failed for: {file_path}")

if __name__ == "__main__":
    main()
