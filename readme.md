# CastlePig Encryption Suite

## Overview

**CastlePig** is a modular, educational Python project for secure file encryption and decryption.  
It uses strong cryptography, secure password storage (via your OS keyring), and can automate itself with Windows Task Scheduler.

---

## Features

- **Strong AES-GCM encryption** with password-based key derivation (PBKDF2)
- **Cryptographically secure password generation**
- **Password storage in your OS keyring** (never in plaintext)
- **Automatic file encryption** (with options to delete originals and move encrypted files)
- **Task Scheduler integration** (auto-run on Windows logon)
- **Modular design** for easy extension and learning

---

## Requirements

- Python 3.7+
- [cryptography](https://pypi.org/project/cryptography/)
- [keyring](https://pypi.org/project/keyring/)

Install dependencies:
```sh
pip install cryptography keyring
```

## Modules

- **file_encrypter.py**
 - Encrypts files, optionally deletes originals, and moves encrypted files to a folder.

 - **file_decrypter.py**
  - Decrypts files encrypted by file_encrypter.py.

 - **secure_password.py**
  - Generates strong, random passwords for encryption.

 - **keyring_password.py**
  - Saves and loads passwords securely using your OS keyring.

 - **task_scheduler.py**
  - Adds your script to Windows Task Scheduler for auto-run at logon.

## Usage

  - 1. Configure Your Script :
    Edit your main script to set:
    SERVICE_NAME and USERNAME (for keyring)
    edit castlepig.py
      ```SERVICE_NAME = "CastlePig"
          USERNAME = "one_dumb_pig"
          files = [
              "example1.txt",
              "example2.txt"
          ]
      ```
