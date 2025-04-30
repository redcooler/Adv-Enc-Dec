import keyring
import argparse
import getpass
import sys

def save_password_to_keyring(password, service_name="MyEncryptionApp", username="encryption_password"):
    if not password:
        raise ValueError("Password cannot be empty.")
    keyring.set_password(service_name, username, password)
    print(f"Password saved securely in the system keyring (service: '{service_name}', username: '{username}').")

def load_password_from_keyring(service_name="MyEncryptionApp", username="encryption_password"):
    password = keyring.get_password(service_name, username)
    if password is None:
        raise ValueError(f"No password found in keyring for service '{service_name}' and username '{username}'.")
    return password

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Save or load a password from the system keyring.")
    parser.add_argument("action", choices=["save", "load"], help="Action to perform: save or load the password.")
    parser.add_argument("--service", default="MyEncryptionApp", help="Service name (default: MyEncryptionApp)")
    parser.add_argument("--username", default="encryption_password", help="Username/label (default: encryption_password)")

    args = parser.parse_args()

    try:
        if args.action == "save":
            pw = getpass.getpass("Enter a password to store in keyring: ")
            save_password_to_keyring(pw, service_name=args.service, username=args.username)
        elif args.action == "load":
            pw = load_password_from_keyring(service_name=args.service, username=args.username)
            print(f"Retrieved password: {pw}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
