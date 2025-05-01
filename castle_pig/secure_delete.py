# castle_pig/secure_delete.py

import os
import sys
import subprocess

def secure_delete(file_path):
    """
    Securely deletes a file using Windows cipher /w: command.
    On non-Windows systems, falls back to standard deletion.
    Returns True if deletion was successful, False otherwise.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    try:
        if sys.platform.startswith('win'):
            print(f"Attempting secure deletion of: {file_path} using cipher...")
            file_directory = os.path.dirname(file_path) or "."
            try:
                # Wipe free space in the directory
                subprocess.run(['cipher', '/w:' + file_directory], check=True, shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"Cipher /w: completed for directory: {file_directory}")
            except subprocess.CalledProcessError as e:
                print(f"Error during cipher wipe: {e}")
                return False
        # Remove the file itself
        os.remove(file_path)
        print(f"File deleted: {file_path}")
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Securely delete a file using cipher (Windows) or standard delete (other OS).")
    parser.add_argument("file", help="Path to the file to securely delete")
    args = parser.parse_args()
    success = secure_delete(args.file)
    if success:
        print("Secure deletion successful.")
    else:
        print("Secure deletion failed.")
