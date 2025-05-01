# file_encrypter.py

import os
import sys
import argparse # Needed for command-line parsing
import shutil
import subprocess # Import subprocess for running external commands
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
    if not os.path.isdir(directory):
        # Print error to stderr, suitable for command line or module use
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
    Optionally deletes the original securely using Windows cipher command
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
                # Continue without moving if moving fails

        # Delete original securely if requested (Windows only)
        if delete_original:
            if sys.platform.startswith('win'): # Check if running on Windows
                print(f"Attempting secure deletion of original file: {file_path} using cipher...")
                try:
                    # Get the directory of the file
                    file_directory = os.path.dirname(file_path)
                    if not file_directory: # If it's in the current directory
                        file_directory = "."

                    # Use cipher /w: to wipe free space in the directory
                    process = subprocess.run(['cipher', '/w:' + file_directory], check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print(f"Cipher /w: completed for directory: {file_directory}")
                    # Optional: print cipher output if needed for debugging
                    # print("Cipher stdout:", process.stdout.decode())
                    # print("Cipher stderr:", process.stderr.decode())

                    # Now safely remove the file itself
                    os.remove(file_path)
                    print(f"Original file deleted: {file_path}")

                except FileNotFoundError:
                    print(f"Original file not found for deletion: {file_path}", file=sys.stderr)
                except subprocess.CalledProcessError as e:
                    print(f"Error during secure deletion with cipher: {e}", file=sys.stderr)
                    print("Please ensure you have necessary permissions to run cipher.", file=sys.stderr)
                    # Optional: print cipher output on error
                    # print("Cipher stdout on error:", e.stdout.decode())
                    # print("Cipher stderr on error:", e.stderr.decode())
                except OSError as e:
                    print(f"Error deleting file after cipher: {e}", file=sys.stderr)
                except Exception as e:
                    print(f"An unexpected error occurred during secure deletion: {e}", file=sys.stderr)
            else:
                print(f"Secure deletion with cipher is only supported on Windows. Skipping secure deletion for {file_path}.", file=sys.stderr)
                # Fallback to standard delete for non-Windows
                try:
                    os.remove(file_path)
                    print(f"Deleted original (standard delete): {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}", file=sys.stderr)

        return encrypted_file_path
    except Exception as e:
        print(f"Error encrypting file: {e}", file=sys.stderr)
        return None

# --- Command-line interface for standalone use ---
# This part runs ONLY when the script is executed directly.
def main():
    parser = argparse.ArgumentParser(description='Encrypt a file or all files in a directory.')
    parser.add_argument('file', nargs='?', help='File to encrypt')
    parser.add_argument('--dir', help='Encrypt all files in this directory')
    parser.add_argument('--password', default=DEFAULT_PASSWORD, help='Password for encryption')
    parser.add_argument('--delete-original', action='store_true', help='Delete original file(s) after encryption (Windows only)')
    parser.add_argument('--move-to', help='Move encrypted file(s) to this folder')
    args = parser.parse_args()

    files_to_process = []

    if args.dir:
        # Use the get_files_from_directory function defined above
        files_to_process = get_files_from_directory(args.dir)
        if not files_to_process:
            print(f"No files found in directory '{args.dir}' to encrypt.")
            sys.exit(0)
    elif args.file:
        # Check if the single file exists
        if not os.path.exists(args.file):
             print(f"Error: File '{args.file}' not found.")
             sys.exit(1)
        files_to_process = [args.file]
    else:
        print("Error: Please specify a file or directory to encrypt.", file=sys.stderr)
        sys.exit(1)

    # Get password, using default if not provided
    encryption_password = args.password if args.password else DEFAULT_PASSWORD

    for file_path in files_to_process:
        # Call the encrypt_file function defined above
        result_file = encrypt_file(
            file_path,
            password=encryption_password,
            delete_original=args.delete_original, # Pass the command-line argument to the function
            move_to_folder=args.move_to
        )
        if result_file:
            print(f"File encrypted successfully: {result_file}")
        else:
            print(f"Encryption failed for: {file_path}")

# This block ensures that main() is only called when the script is executed directly
if __name__ == "__main__":
    main()
