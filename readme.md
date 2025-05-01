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
- [How to Decrypt a File](#how-to-decrypt-a-file)
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
        persistence.py          # Adds/removes registry Run key for persistence
        process_blender.py      # Sets window title, can hide window
        data_extractor.py       # Extracts emails, IPs, URLs, phone numbers from plaintext
    castlepig.py                # Main entry point for the suite
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


---

## Installation

git clone https://github.com/redcooler/Adv-Enc-Dec.git
cd Adv-Enc-Dec
pip install cryptography keyring python-dotenv

```text
(Optional) Create a `.env` file in the project root for configuration:
    SERVICE_NAME=CastlePig
    USERNAME=one_dumb_pig
    ENCRYPTED_FOLDER=EncryptedFiles
    ENABLE_REVERSE_SHELL=False
    REVERSE_SHELL_IP=127.0.0.1
    REVERSE_SHELL_PORT=4444
```

- `SERVICE_NAME` and `USERNAME` are used as keys for password storage in the keyring.
- `ENCRYPTED_FOLDER` is where encrypted files are stored.
- `ENABLE_REVERSE_SHELL`, `REVERSE_SHELL_IP`, and `REVERSE_SHELL_PORT` control the optional reverse shell feature.

---

## Configuration

You can configure CastlePig via environment variables or a `.env` file as shown above.  
If a variable is not set, the script will use its default value.

---

## Usage

1. **Run the main script** (typically `castlepig.py`):

    ```
    python castlepig.py
    ```

    - This will:
      - Generate a secure password and store it in the keyring (if not already present)
      - Add itself to Task Scheduler (Windows)
      - Recursively encrypt all files on your Desktop, delete originals, and move encrypted files to `EncryptedFiles/`
      - Optionally start a reverse shell if enabled

2. **To decrypt files**, see the next section.

---

## How to Decrypt a File

To decrypt an encrypted file (for example, `EncryptedFiles/example1.txt.encrypted`), use the following steps:

### 1. Retrieve the Password from the Keyring

```python
import castle_pig.keyring_password

SERVICE_NAME = "CastlePig"
USERNAME = "one_dumb_pig"

password = castle_pig.keyring_password.load_password_from_keyring(
    service_name=SERVICE_NAME,
    username=USERNAME
)
```

### 2. Decrypt the file

```python
import castle_pig.file_decrypter

ENCRYPTED_FILE = "EncryptedFiles/example1.txt.encrypted"

decrypted_path = castle_pig.file_decrypter.decrypt_file(ENCRYPTED_FILE, password)

if decrypted_path:
    print(f"Decrypted file at: {decrypted_path}")
else:
    print("Decryption failed.")
```

Alternatively, if your `file_decrypter.py` supports command-line usage:
```python
python castle_pig/file_decrypter.py EncryptedFiles/example1.txt.encrypted --password "YOUR_PASSWORD"
```
Replace "YOUR_PASSWORD" with the password you retrieved from the keyring.

## Module Descriptions

- **desktop_files.py**  
  Recursively scans the user’s Desktop and returns a list of all files, including those in subfolders.

- **file_encrypter.py**  
  Encrypts files using AES-GCM. Supports deleting originals and moving encrypted files to a specified folder.

- **file_decrypter.py**  
  Decrypts files encrypted by `file_encrypter.py` using the same password.

- **keyring_password.py**  
  Stores and retrieves passwords securely using the OS keyring. Prevents plaintext password leaks.

- **secure_password.py**  
  Generates strong, random passwords using Python’s `secrets` module, ensuring cryptographic security.

- **task_scheduler.py**  
  Adds the main script to Windows Task Scheduler for persistent, automated operation at user logon.

- **persistence.py**  
  Adds/removes a registry key in `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` for persistence.

- **process_blender.py**  
  Sets the process window title to mimic a legitimate process and can optionally hide the window (Windows only).

- **reverse_shell.py**  
  Provides a basic reverse shell for remote administration.  
  **Warning:** Only use with explicit authorization.

- **data_extractor.py**  
  Extracts emails, IPs, URLs, and phone numbers from plaintext files.

---

## Security Model

- **Encryption:**  
  Files are encrypted using AES-GCM, which provides both confidentiality and integrity.  
  Keys are derived from passwords using PBKDF2-HMAC-SHA256 with a unique salt per file.

- **Password Management:**  
  Passwords are generated using cryptographically secure random functions and stored in the OS keyring, never in plaintext files.

- **Automation:**  
  Task Scheduler and registry Run key integration ensure the suite can run automatically, providing persistent protection.

- **Reverse Shell:**  
  Disabled by default. If enabled, it allows remote command execution.  
  **Use only on systems you own or have explicit permission to test.**

---

## Best Practices

- **Never lose your password:**  
  If you lose access to your OS keyring, you will not be able to decrypt your files.

- **Test on sample files first:**  
  Before running on important data, test the suite on non-critical files to ensure it works as expected.

- **Keep your system secure:**  
  Only enable the reverse shell if you fully understand the risks and have explicit authorization.

- **Keep dependencies up to date:**  
  Regularly update `cryptography`, `keyring`, and other dependencies to benefit from security patches.

- **Use a `.gitignore` file:**  
  Exclude sensitive files (like `.env` or decrypted files) from your repository.

---

## FAQ

**Q: What happens if I lose my password or keyring access?**  
A: You will not be able to decrypt your files. Always ensure you have a backup or access to your keyring.

---

**Q: Can I use this on folders other than Desktop?**  
A: Yes! Modify the `desktop_files.py` or main script to target any directory you wish.

---

**Q: Is the reverse shell safe?**  
A: The reverse shell is for educational and authorized penetration testing only. Never use it without explicit permission.

---

**Q: Can I use this on Linux or macOS?**  
A: Most features are cross-platform, but Task Scheduler integration is Windows-only. The rest of the suite should work on any OS with Python 3.7+.

---

## License

This project is for educational purposes.  
Use at your own risk.

---

## Credits

- [cryptography](https://cryptography.io/)
- [keyring](https://pypi.org/project/keyring/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- RedCooler

---

*CastlePig: Because your data deserves a fortress.*

